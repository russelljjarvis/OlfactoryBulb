import os
import json
from prev_ob_models.Birgiolas2020.isolated_cells import *
from blenderneuron.nrn.neuronnode import NeuronNode
from database import Odor, OdorGlom, CellModel
from math import pow

class OlfactoryBulb:
    def __init__(self, slice_name):
        self.slice_dir = os.path.abspath(os.path.join('olfactorybulb', 'slices', slice_name))
        self.cells = {}
        self.inputs = []
        self.bn_server = NeuronNode()

        for cell_type in ['MC', 'GC', 'TC']:
            self.load_cells(cell_type)

        for synapse_set in ['GCs__MCs', 'GCs__TCs']:
            self.load_synapse_set(synapse_set)

        # Load glom->cell links
        self.load_glom_cells()

        from neuron import h
        self.h = h

        # DEBUG - set syn weights to instant APs
        [setattr(s, 'gmax', 1E2) for s in h.AmpaNmdaSyn]
        [setattr(s, 'gmax', 1E2) for s in h.GabaSyn]

        self.add_inputs(odor='Apple', t=20, rel_conc=1.0)

        h.tstop = 50

    def add_inputs(self, odor='Apple', t=20, rel_conc=1.0):

        # Get all the different cell models used in the slice
        input_models = set()
        for cells in self.glom_cells.values():
            for cell in cells:
                input_models.add(cell[:cell.find('[')])

        # Get each model's input segments (in the tuft)
        model_inputsegs = { m.class_name: m.tufted_dend_root
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
            input_segs = ['h.' + cell + '.' + model_inputsegs[cell[:cell.find('[')]] for cell in cells]
            intensity = glom_intensities[glom_id] * rel_conc
            self.stim_glom_segments(t, input_segs, intensity)

    def load_glom_cells(self):
        with open(os.path.join(self.slice_dir, 'glom_cells.json')) as f:
            self.glom_cells = json.load(f)

    def stim_glom_segments(self, time, input_segs, intensity):
        h = self.h

        delay = pow(intensity, -3.57)
        gmax = intensity * 1.0

        for seg_name in input_segs:
            # Create synapse point process
            seg = eval(seg_name)
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
                gmax  # weight
            )

            self.inputs.append((syn, ns, netcon))

    def load_cells(self, cell_type):

        # Load the cell json file
        path = os.path.join(self.slice_dir, cell_type + 's.json')

        with open(path, 'r') as f:
            group_dict = json.load(f)

        # Count how many of each cell model we have
        cell_counts = {}

        for root in group_dict['roots']:
            name = root['name']
            name = name[0:name.find('[')]

            count = cell_counts.get(name, 0)
            count += 1

            cell_counts[name] = count

        # Load that many base instances of each model
        self.cells[cell_type] = []
        for cell_model_name, count in cell_counts.items():
            cell_models = [eval(cell_model_name + '()') for _ in range(count)]
            self.cells[cell_type].extend(cell_models)

        # Update section index with the new cells
        self.bn_server.update_section_index()

        # Apply the cell json file onto the base instances
        self.bn_server.update_groups([group_dict])

    def load_synapse_set(self, synapse_set):
        path = os.path.join(self.slice_dir, synapse_set + '.json')

        with open(path, 'r') as f:
            synapse_set_dict = json.load(f)

        self.bn_server.create_synapses(synapse_set_dict)

