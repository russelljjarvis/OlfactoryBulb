from prev_ob_models.Birgiolas2020.isolated_cells import *
from olfactorybulb.database import CellModel, Odor, OdorGlom


class SliceBuilderNRN:
    def __init__(self):
        # Load NRN
        from neuron import h, gui

        # Connect to Blender addon
        from blenderneuron.neuronstart import BlenderNEURON as addon

        # Add methods that can be called from Blender
        addon.server.register_function(self.get_base_model_info)
        addon.server.register_function(self.create_cell)
        addon.server.register_function(self.get_odor_gloms)

        # Keep track of cells
        self.cells = {
            "MC": [],
            "TC": [],
            "GC": [],
        }

    def get_base_model_info(self):
        mc_base_models = self.get_model_info('MC')
        tc_base_models = self.get_model_info('TC')
        gc_base_models = self.get_model_info('GC')

        return mc_base_models, tc_base_models, gc_base_models

    def get_model_info(self, cell_type='MC'):
        return {
            cm["class_name"]: cm for cm in CellModel \
            .select() \
            .where((CellModel.source_id == 'Birgiolas (2020)') & (CellModel.cell_type == cell_type)) \
            .order_by(CellModel.class_name)
            .dicts() \
            }

    def create_cell(self, type, class_name):
        exec ("cell = " + class_name + "()")

        self.cells[type].append(cell)

        return str(cell.soma.name())

    def get_odor_gloms(self, odors):
        if odors == 'all':
            return None

        result = set()

        for odor in odors:
            odor_gloms = OdorGlom \
                .select(OdorGlom.glom_id) \
                .distinct() \
                .join(Odor) \
                .where(Odor.name == odor)

            for glom in odor_gloms:
                result.add(glom.glom_id)

        return list(result)
