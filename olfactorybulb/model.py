import os
import json
from prev_ob_models.Birgiolas2020.isolated_cells import *
from blenderneuron.nrn.neuronnode import NeuronNode
from database import Odor, OdorGlom, CellModel, database
from math import pow
from LFPsim.LFPsimpy import LfpElectrode
import sys
from heapq import *

class OlfactoryBulb:
    def __init__(self, slice_name):
        self.slice_dir = os.path.abspath(os.path.join('olfactorybulb', 'slices', slice_name))
        self.cells = {}
        self.inputs = []
        self.bn_server = NeuronNode()
        self.bn_server.stop_server()

        from neuron import h, load_mechanisms
        self.h = h
        self.pc = h.ParallelContext()
        self.mpimap = {}
        self.nranks = self.pc.nhost()
        self.mpirank = self.pc.id()

        # Keep track of rank complexities with a min-heap
        self.rank_complexities = [(0, r) for r in range(self.nranks)]

        for cell_type in ['MC', 'GC', 'TC']:
            self.load_cells(cell_type)

        if self.mpirank == 0:
            print('Rank Complexities:' + str(self.rank_complexities))

        for synapse_set in ['GCs__MCs', 'GCs__TCs']:
            self.load_synapse_set(synapse_set)

        # Load glom->cell links
        self.load_glom_cells()

        # DEBUG - set syn weights to instant APs
        if hasattr(h, 'GabaSyn'):
            [setattr(s, 'gmax', 1.5E1) for s in h.AmpaNmdaSyn]
            [setattr(s, 'gmax', 1E1) for s in h.GabaSyn]

        self.add_inputs(odor='Apple', t=100, rel_conc=0.009)

        # LFP
        # Inside dorsal Granule Layer
        # Approximaly to where it was located in Manabe & Mori (2013)
        # In adult male Long-Evans rat:
        # 8.0 mm anterior to the bregma
        # 1.3 mm lateral to the midline
        # 2.5 mm from the skull surface
        self.electrode = self.create_lfp_electrode(116, 1078, -61)

        self.setup_status_reporter()

        if self.mpirank == 0 and self.nranks == 1:
            from neuron import gui
            h.load_file('1x1x1-testbed.ses')

            h.newPlotI()
            [g for g in h.Graph][-1].addvar('LFPsimpy[0].value')

        self.run(200.1)  # ms

        if self.mpirank == 0:
            t, lfp = self.get_lfp()

            from matplotlib import pyplot as plt
            plt.plot(t, lfp)
            plt.show()
            pass

        database.close()

    def run(self, tstop):

        h = self.h
        h.dt = 1/8.0
        h.tstop = tstop

        if self.nranks == 1:
            h.run()

        else:
            self.pc.timeout(1)
            h.cvode.cache_efficient(1)
            h.cvode_active(0)
            self.pc.set_maxstep(1)
            h.stdinit()
            self.pc.psolve(h.tstop)

    def print_status(self):
        sys.stdout.write("\rTime: %s ms" % self.h.t)
        sys.stdout.flush()

    def setup_status_reporter(self):
        if self.mpirank == 0:
            h = self.h

            collector_stim = h.NetStim(0.5)
            collector_stim.start = 0
            collector_stim.interval = 1
            collector_stim.number = 1e9
            collector_stim.noise = 0

            collector_con = h.NetCon(collector_stim, None)
            collector_con.record(self.print_status)

            self.collector_stim = collector_stim
            self.collector_con = collector_con

    def create_lfp_electrode(self, x, y, z, sampling_period=0.1, method='Line'):
        return LfpElectrode(x, y, z, sampling_period, method)

    def get_lfp(self):
        if self.electrode is None or not any(self.electrode.times):
            raise Exception('Run simulation first to get the LFP')

        t = self.electrode.times
        lfp = self.electrode.values

        import cPickle
        with open('lfp.pkl', 'w') as f:
            cPickle.dump((t, lfp), f)

        return t, lfp

    def add_inputs(self, odor, t, rel_conc):

        # Get all the different cell models used in the slice
        input_models = set()
        for cells in self.glom_cells.values():
            for cell in cells:
                input_models.add(cell[:cell.find('[')])

        # Get each model's input segments (in the tuft)
        model_inputsegs = {m.class_name: m.tufted_dend_root
                           for m in CellModel \
                               .select(CellModel.class_name, CellModel.tufted_dend_root) \
                               .where(CellModel.class_name.in_(list(input_models)))}

        # Get input odor glomeruli
        glom_intensities = {g.glom_id: g.intensity \
                            for g in OdorGlom \
                                .select(OdorGlom.glom_id, OdorGlom.intensity) \
                                .join(Odor) \
                                .where(Odor.name == odor)}

        for glom_id, cells in self.glom_cells.items():
            glom_id = int(glom_id)

            input_segs = []
            for cell in cells:
                rank_cell = self.bn_server.rank_section_name(cell)

                # Add inputs only to cells that are on this rank
                if rank_cell is None:
                    continue

                model_class = rank_cell[:rank_cell.find('[')]
                input_seg = model_inputsegs[model_class]
                seg_address = 'h.' + rank_cell + '.' + input_seg

                input_segs.append(seg_address)

            if len(input_segs) > 0:
                glom_intensity = glom_intensities[glom_id] * rel_conc
                self.stim_glom_segments(t, input_segs, glom_intensity)

    def load_glom_cells(self):
        with open(os.path.join(self.slice_dir, 'glom_cells.json')) as f:
            self.glom_cells = json.load(f)

    def stim_glom_segments(self, time, input_segs, intensity):
        h = self.h

        # delay = pow(intensity, -3.57)
        delay = 0
        weight = intensity * 1.0

        for seg_name in input_segs:
            # Create synapse point process
            seg = eval(seg_name.replace('(1)', '(.999)'))
            syn = h.Exp2Syn(seg)
            syn.tau1 = 20
            syn.tau2 = 200

            # Netstim to send the input
            ns = h.NetStim()
            ns.number = 1
            ns.start = time
            ns.noise = 0

            # Netcon to trigger the synapse
            netcon = h.NetCon(
                ns,
                syn,
                0,  # thresh
                delay,
                weight  # weight
            )

            self.inputs.append((syn, ns, netcon))

    def load_cells(self, cell_type):

        # Load the cell json file
        path = os.path.join(self.slice_dir, cell_type + 's.json')

        with open(path, 'r') as f:
            group_dict = json.load(f)

        # Count how many of each cell model will be on each rank
        rank_cell_counts = {r: {} for r in range(self.nranks)}

        for ri, root in enumerate(group_dict['roots']):
            # Get the least loaded rank
            min_complexity, min_complexity_rank = heappop(self.rank_complexities)

            # Cell nseg count is used as a proxy for complexity
            nsegs = self.get_nseg_count(root)

            # Add to rank complexity and push back onto the heap
            heappush(self.rank_complexities, (min_complexity+nsegs, min_complexity_rank))

            # Assign cell to least busy rank
            cell_rank = min_complexity_rank
            # # Round robin assignment of cells to ranks
            # cell_rank = ri % self.nranks

            name = root['name']
            name = name[0:name.find('[')]

            count = rank_cell_counts[cell_rank].get(name, 0)

            self.mpimap[root['name'][:root['name'].find(']')+1]] = {
                'name': name + '[' + str(count * 2) + ']',
                'rank': cell_rank
            }

            count += 1
            rank_cell_counts[cell_rank][name] = count

        # Load that many base instances of each model
        self.cells[cell_type] = []
        for cell_model_name, count in rank_cell_counts[self.mpirank].items():
            cell_models = [eval(cell_model_name + '()') for _ in range(count)]
            self.cells[cell_type].extend(cell_models)

        # Update section index with the new cells
        self.bn_server.update_section_index()

        # Apply the cell json file onto the base instances
        self.bn_server.init_mpi(self.pc, self.mpimap)
        self.bn_server.update_groups([group_dict])

    def get_nseg_count(self, root_dict):
        count = root_dict["nseg"]

        for child_dict in root_dict['children']:
            count += self.get_nseg_count(child_dict)

        return count

    def load_synapse_set(self, synapse_set):
        path = os.path.join(self.slice_dir, synapse_set + '.json')

        with open(path, 'r') as f:
            synapse_set_dict = json.load(f)

        self.bn_server.create_synapses(synapse_set_dict)
