try:
    import cPickle # Python 2
except:
    import pickle as cPickle # Python 3

import os
import numpy as np
import json
from prev_ob_models.Birgiolas2020.isolated_cells import *
from blenderneuron.nrn.neuronnode import NeuronNode
from database import Odor, OdorGlom, CellModel, database
from math import pow
from LFPsimpy.LFPsimpy import LfpElectrode
import sys
from heapq import *
from matplotlib import pyplot as plt
from hashlib import sha1
from random import random, seed

from olfactorybulb.paramsets.base import *
from olfactorybulb.paramsets.case_studies import *
from olfactorybulb.paramsets.sensitivity import *


class OlfactoryBulb:
    def __init__(self, params="ParameterSetBase", autorun=True):
        if type(params) == str:
            params = eval(params)()

        self.params = params

        self.rnd_seed = params.rnd_seed

        self.slice_dir = os.path.abspath(os.path.join(params.slice_dir, params.slice_name))
        self.cells = {}
        self.inputs = []

        self.gj_source_gids = set()
        self.gjs = []

        # Just use the BlenderNEURON package functions (e.g. no server/client)
        self.bn_server = NeuronNode(end='Package')

        from neuron import h, load_mechanisms
        self.h = h
        self.pc = h.ParallelContext()
        self.mpimap = {}
        self.nranks = int(self.pc.nhost())
        self.mpirank = self.pc.id()

        # Keep track of rank complexities with a min-heap
        self.rank_complexities = [(0, r) for r in range(self.nranks)]

        self.t_vec = h.Vector()
        self.t_vec.record(h._ref_t, params.recording_period)
        self.v_vectors = {}
        self.input_vectors = []

        for cell_type in ['MC', 'GC', 'TC']:
            self.load_cells(cell_type)

        if self.mpirank == 0:
            complexities = np.array([c[0] for c in self.rank_complexities])
            min = np.min(complexities)
            max = np.max(complexities)
            mean = np.mean(complexities)

            print('Rank Complexity min: %s, mean: %s, max: %s' % (min, mean, max))

        for synapse_set in ['GCs__MCs', 'GCs__TCs']:
            self.load_synapse_set(synapse_set)

        # Load glom->cell links
        self.load_glom_cells()

        # Create gap junctions between MC and TC tufts
        for cell_type, g_gap in params.gap_juction_gmax.items():
            self.add_gap_junctions(cell_type, g_gap)

        # Set synapse parameters
        for syn_mech, syn_values in params.synapse_properties.items():
            if hasattr(h, syn_mech):
                for syn_attrib, attrib_value in syn_values.items():
                    [setattr(s, syn_attrib, attrib_value) for s in getattr(h, syn_mech)]

        # Add glomerular inputs
        for time, odor_info in params.input_odors.items():
            self.add_inputs(odor=odor_info["name"], t=time, rel_conc=odor_info["rel_conc"])

        # LFP
        self.electrode = self.create_lfp_electrode(*params.lfp_electrode_location,
                                                   sampling_period=params.recording_period)

        self.setup_status_reporter()

        for cell_type in params.record_from_somas:
            self.record_from_somas(cell_type)

        if self.mpirank == 0 and self.nranks == 1:
            from neuron import gui
            # h.load_file('1x1x1-testbed.ses')

            h.newPlotI()
            [g for g in h.Graph][-1].addvar('LfpElectrode[0].value')

        if autorun:
            self.run(params.tstop)

            if self.mpirank == 0:
                self.results_dir = os.path.join('olfactorybulb', 'results', params.name)
                if not os.path.exists(self.results_dir):
                    os.makedirs(self.results_dir)

            self.save_recorded_vectors()

            if self.mpirank == 0:
                t, lfp = self.get_lfp()

            # Cleanup on MPI
            if self.nranks > 1:
                database.close()
                self.h.quit()


    def stim_glom_segments(self, time, input_segs, intensity):
        h = self.h

        inhale_duration = self.params.inhale_duration

        # ORN firing rate
        max_firing_rate = self.params.max_firing_rate

        # Translate intensity to number of spikes per inhalation
        spike_count = int(round(max_firing_rate * intensity * (inhale_duration / 1000.0)))

        for seg_name, seg_gid, single_rank_seg_name in input_segs:
            # Randomize spikes to each tufted segment
            seed_source = "%s|%s|%s|%s" % (self.rnd_seed, time, single_rank_seg_name, intensity)
            np.random.seed(self.stable_hash(seed_source))

            # Odor is modeled as a gaussian spike train representing OSN spikes during inhalation
            # exhalation is assumed to not generate OSN spikes
            spike_times = self.get_gaussian_spike_train(spike_count, time, inhale_duration)

            # Create synapse point process
            seg = eval(seg_name.replace('(1)', '(.999)'))
            syn = h.Exp2Syn(seg)
            syn.tau1 = self.params.input_syn_tau1
            syn.tau2 = self.params.input_syn_tau2

            if "MC" in seg_name:  # MCs
                delay = self.params.mc_input_delay
                weight = self.params.mc_input_weight

            else:  # "TC"
                delay = self.params.tc_input_delay
                weight = self.params.tc_input_weight

            # VecStim will deliver events to synapse at vector times
            ns = h.VecStim()
            ns.play(h.Vector(spike_times + delay))

            # Netcon to trigger the synapse
            netcon = h.NetCon(
                ns,
                syn,
                0,  # thresh
                0,  # delay
                weight  # weight uS
            )

            # Record odor input events
            input_vec = h.Vector()
            netcon.record(input_vec)
            self.input_vectors.append((single_rank_seg_name, input_vec))

            self.inputs.append((syn, ns, netcon))

    def stable_hash(self, source, digits=9):
        return int(sha1(source).hexdigest(), 16) % (10 ** digits)

    def run(self, tstop):
        if self.mpirank == 0:
            print('Starting simulation...')

        h = self.h
        h.dt = self.params.sim_dt
        h.tstop = tstop

        if self.nranks == 1:
            h.cvode_active(0)
            h.cvode.cache_efficient(1)
            h.run()

        else:
            self.pc.setup_transfer()
            self.pc.timeout(1)
            # h.cvode.cache_efficient(0) # This line causes gap junction Seg Faults
            h.cvode_active(0)
            self.pc.set_maxstep(1)
            h.stdinit()
            self.pc.psolve(h.tstop)

        # Clear status updater line
        if self.mpirank == 0:
            print('')

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

    def create_lfp_electrode(self, x, y, z, sampling_period, method='Line'):
        return LfpElectrode(x, y, z, sampling_period, method)

    def get_lfp(self):
        if self.electrode is None or not any(self.electrode.times):
            raise Exception('Run simulation first to get the LFP')

        t = self.electrode.times
        lfp = self.electrode.values

        import cPickle
        with open(os.path.join(self.results_dir, 'lfp.pkl'), 'w') as f:
            cPickle.dump((t, lfp), f)

        return t, lfp

    def get_model_inputsegs(self):

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

        return model_inputsegs

    def add_gap_junctions(self, in_name, g_gap):

        model_inputsegs = self.get_model_inputsegs()

        for glom_id, cells in self.glom_cells.items():

            input_segs = []
            for cell in cells:
                if in_name not in cell:
                    continue

                model_class = cell[:cell.find('[')]
                input_seg = model_inputsegs[model_class]

                single_rank_address = 'h.' + cell + '.' + input_seg
                single_rank_gid = self.stable_hash(single_rank_address)

                rank_cell = self.bn_server.rank_section_name(cell)

                if rank_cell is not None:
                    seg_address = 'h.' + rank_cell + '.' + input_seg
                else:
                    seg_address = None

                input_segs.append((seg_address, single_rank_gid))

            if len(input_segs) > 0:
                self.create_gap_junctions_between(input_segs, g_gap)

        self.pc.setup_transfer()

    def create_gap_junctions_between(self, input_segs, g_gap):
        count = len(input_segs)

        if count < 2:
            return

        h = self.h

        first_seg = input_segs[0]
        last_seg = input_segs[-1]

        if count > 2:
            for i, seg in enumerate(input_segs[:-1]):
                next_seg = input_segs[i + 1]

                self.create_gap_junction(seg, next_seg, g_gap)

        self.create_gap_junction(first_seg, last_seg, g_gap)

    def create_gap_junction(self, seg_1_info, seg_2_info, g_gap):
        h = self.h

        seg_1_name, seg_1_gid = seg_1_info
        seg_2_name, seg_2_gid = seg_2_info

        if seg_1_name is not None:
            seg1 = eval(seg_1_name.replace('(1)', '(.999)'))

            if seg_1_gid not in self.gj_source_gids:
                self.pc.source_var(seg1._ref_v, seg_1_gid, sec=seg1.sec)
                self.gj_source_gids.add(seg_1_gid)

            gap1 = h.GapJunction(seg1.x, sec=seg1.sec)
            gap1.g = g_gap
            self.pc.target_var(gap1._ref_v_other, seg_2_gid)
            self.gjs.append(gap1)

        if seg_2_name is not None:
            seg2 = eval(seg_2_name.replace('(1)', '(.999)'))

            if seg_2_gid not in self.gj_source_gids:
                self.pc.source_var(seg2._ref_v, seg_2_gid, sec=seg2.sec)
                self.gj_source_gids.add(seg_2_gid)

            gap2 = h.GapJunction(seg2)
            gap2.g = g_gap
            self.pc.target_var(gap2._ref_v_other, seg_1_gid)
            self.gjs.append(gap2)



    def add_inputs(self, odor, t, rel_conc):

        model_inputsegs = self.get_model_inputsegs()

        # Get input odor glomeruli
        glom_intensities = {g.glom_id: g.intensity
                            for g in OdorGlom
                                .select(OdorGlom.glom_id, OdorGlom.intensity)
                                .join(Odor)
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

                single_rank_address = 'h.' + cell + '.' + input_seg
                single_rank_gid = int(sha1(single_rank_address).hexdigest(), 16) % (10 ** 9)

                input_segs.append((seg_address, single_rank_gid, single_rank_address))

            if len(input_segs) > 0:
                glom_intensity = glom_intensities[glom_id] * rel_conc
                self.stim_glom_segments(t, input_segs, glom_intensity)

    def load_glom_cells(self):
        with open(os.path.join(self.slice_dir, 'glom_cells.json')) as f:
            self.glom_cells = json.load(f)

    def get_gaussian_spike_train(self, spikes=50, start_time=100, duration=10):

        # Create a gaussian whose 99% range starts at start_time
        # and ends at start_time + duration
        normal_stdev = duration / (2.576 * 2)
        normal_mean = start_time + duration / 2.0

        times = np.random.normal(start_time + (duration / 2.0), normal_stdev, spikes)

        # Remove any spikes outside this range
        times = times[np.where((times > start_time) & (times < start_time + duration))]
        times.sort()

        return times

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
            heappush(self.rank_complexities, (min_complexity + nsegs, min_complexity_rank))

            # Assign cell to least busy rank
            cell_rank = min_complexity_rank
            # # Round robin assignment of cells to ranks
            # cell_rank = ri % self.nranks

            name = root['name']
            name = name[0:name.find('[')]

            count = rank_cell_counts[cell_rank].get(name, 0)

            self.mpimap[root['name'][:root['name'].find(']') + 1]] = {
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

    def record_from_somas(self, cell_type):
        h = self.h

        for cell_model in self.cells[cell_type]:
            v_vec = h.Vector()
            v_vec.record(cell_model.soma(0.5)._ref_v, self.params.recording_period)
            self.v_vectors[str(cell_model.soma)] = v_vec

    def save_recorded_vectors(self):
        # Gather cell voltage vectors
        all_v_vecs = self.pc.py_gather(self.v_vectors, 0)

        if all_v_vecs is not None:
            t = self.t_vec.to_python()
            result = []
            for rank_v_vecs in all_v_vecs:
                for cell, v_vec in rank_v_vecs.items():
                    result.append((cell, t, v_vec.to_python()))

            with open(os.path.join(self.results_dir, 'soma_vs.pkl'), 'w') as f:
                cPickle.dump(result, f)

        # Gather input event time vectors
        all_input_vecs = self.pc.py_gather(self.input_vectors, 0)

        if all_input_vecs is not None:
            result = []
            for rank_input_vecs in all_input_vecs:
                for seg_name, t_vec in rank_input_vecs:
                    result.append((seg_name, t_vec.to_python()))

            with open(os.path.join(self.results_dir, 'input_times.pkl'), 'w') as f:
                cPickle.dump(result, f)

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
