import bpy, sys, os, time, re
import random
import os, sys
import bpy
import numpy as np
from collections import OrderedDict
from mathutils import Vector
import random
from math import pi
sys.path.append(os.getcwd())
from olfactorybulb import slices
from blenderneuron.blender.utils import fast_get

def auto_start(scene):

    # Remove auto-execute command after starting
    bpy.app.handlers.scene_update_post.remove(auto_start)

    # Assuming starting at repo root
    sys.path.append(os.getcwd())

    # Create a slice builder class
    sbb = bpy.types.Object.SliceBuilder = SliceBuilderBlender()

    sbb.build()

class SliceBuilderBlender:
    @property
    def node(self):
        return bpy.types.Object.BlenderNEURON_node

    @property
    def neuron(self):
        return self.node.client

    @property
    def slice_dir(self):
        slice_dir = os.path.abspath(os.path.dirname(slices.__file__))
        return os.path.join(slice_dir, self.slice_name)

    def __init__(self,
                 slice_object_name='TestSlice',
                 mc_particles_object_name='2 ML Particles',
                 tc_particles_object_name='1 OPL Particles',
                 gc_particles_object_name='4 GRL Particles',
                 glom_particles_object_name='0 GL Particles',
                 outer_opl_object_name='1 OPL-Outer',
                 inner_opl_object_name='1 OPL-Inner'):

        random.seed(0)

        self.slice_name = slice_object_name

        self.glom_particles_name = glom_particles_object_name
        self.tc_particles_name = tc_particles_object_name
        self.mc_particles_name = mc_particles_object_name
        self.gc_particles_name = gc_particles_object_name

        self.outer_opl_object_name = outer_opl_object_name
        self.inner_opl_object_name = inner_opl_object_name

        # Within slice
        self.get_cell_locations()

        self.get_cell_base_model_info()

        # Show as section objects
        self.prepare_group()

        # Clear slice files
        self.clear_slice_files()

    def clear_slice_files(self):
        dir = self.slice_dir

        # Match e.g. 'MC1_0.py'
        pattern = re.compile('.C.+_.+py')

        for file in os.listdir(dir):
            if pattern.match(file) is not None:
                os.remove(os.path.abspath(os.path.join(dir, file)))

    def get_cell_locations(self):
        slice = bpy.data.objects[self.slice_name]

        self.globalize_slice()

        self.mc_locs = self.get_locs_within_slice(self.mc_particles_name, self.slice_name)[:1]
        self.glom_locs = self.get_locs_within_slice(self.glom_particles_name, self.slice_name)
        self.tc_locs = self.get_locs_within_slice(self.tc_particles_name, self.slice_name)[:1]
        self.gc_locs = self.get_locs_within_slice(self.gc_particles_name, self.slice_name)[:1]

        print('Gloms:', len(self.glom_locs))
        print('TCs:', len(self.tc_locs))
        print('MCs:', len(self.mc_locs))
        # print('GCs:', len(self.gc_locs))

    def get_cell_base_model_info(self):
        self.mc_base_models, self.tc_base_models, self.gc_base_models = \
            self.neuron.get_base_model_info()

        self.mc_base_models = OrderedDict(self.mc_base_models)
        self.tc_base_models = OrderedDict(self.tc_base_models)
        self.gc_base_models = OrderedDict(self.gc_base_models)

        self.max_apic_mc_info = self.get_longest_apic_model(self.mc_base_models)
        self.mc_apic_lengths = [mc["apical_dendrite_reach"] for mc in self.mc_base_models.values()]

        self.max_apic_tc_info = self.get_longest_apic_model(self.tc_base_models)
        self.tc_apic_lengths = [tc["apical_dendrite_reach"] for tc in self.tc_base_models.values()]

        self.max_apic_gc_info = self.get_longest_apic_model(self.gc_base_models)
        self.gc_apic_lengths = [gc["apical_dendrite_reach"] for gc in self.gc_base_models.values()]

    def prepare_group(self):
        # show each section as blender objects
        group = self.node.groups.get('Group.000')

        if group is None:
            group = self.node.add_group()

        group.interaction_granularity = 'Section'
        group.recording_granularity = 'Cell'
        group.record_activity = False

    def globalize_slice(self):
        # Apply all/any transformations to the slice
        slice = bpy.data.objects[self.slice_name]
        slice.select = True
        bpy.context.scene.objects.active = slice
        bpy.ops.object.transform_apply(location=True, scale=True, rotation=True)
        slice.select = False

    def build(self):
        for loc in self.mc_locs:
            self.add_mc(loc)

        for loc in self.tc_locs:
            self.add_tc(loc)

        for loc in self.gc_locs:
            self.add_gc(loc)

    def add_mc(self, loc):

        # find the closest glom loc
        glom_dists = self.dist_to_gloms(loc)
        closest_glom_idxs = np.argsort(glom_dists)

        closest_glom_loc = self.glom_locs[closest_glom_idxs][0]
        dist_to_closest_glom = glom_dists[closest_glom_idxs][0]

        longest_apic_reach = self.max_apic_mc_info["apical_dendrite_reach"]

        # Apics are too short - use the longest MC
        if dist_to_closest_glom > longest_apic_reach:
            base_class = self.max_apic_mc_info["class_name"]
            apic_glom_loc = closest_glom_loc

        # Apics are longer than distance
        else:
            # get mcs with apics longer than the closest glom
            longer_idxs = np.where(self.mc_apic_lengths > dist_to_closest_glom)[0]

            # pick a random mc from this list
            rand_idx = longer_idxs[random.randrange(len(longer_idxs))]
            mc_apic_len = self.mc_apic_lengths[rand_idx]
            mc = list(self.mc_base_models.values())[rand_idx]

            # find a glom whose distance is as close to the length of the mc apic
            matching_glom_idx = np.argmin(np.abs(glom_dists - mc_apic_len))
            matching_glom_loc = self.glom_locs[matching_glom_idx]

            base_class = mc["class_name"]
            apic_glom_loc = matching_glom_loc


        # Create the selected MC in NRN
        instance_name = self.neuron.create_cell('MC', base_class)

        # Get updated list of NRN cells in Blender
        bpy.ops.custom.get_cell_list_from_neuron()

        # Select the created instance
        group = self.node.groups['Group.000']
        group.include_roots_by_name([instance_name], exclude_others=True)

        # Import group with the created cell
        bpy.ops.custom.import_selected_groups()

        mc_soma, mc_apic_start, mc_apic_end = \
            self.get_key_mctc_section_objects(self.mc_base_models, base_class, instance_name)

        # Align apical towards the closest glom
        self.position_orient_mctc(mc_soma,
                                  mc_apic_start,
                                  mc_apic_end,
                                  loc,
                                  closest_glom_loc,
                                  apic_glom_loc)


        # Retain the reoriented cell
        bpy.ops.custom.update_groups_from_view()

        # Extend apic to the glom
        self.extend_apic(mc_apic_start, mc_apic_end, apic_glom_loc)

        self.align_dends(group, self.inner_opl_object_name)

        self.save_transform(instance_name, group)

    def add_tc(self, tc_loc):

        # find the closest glom loc
        glom_dists = self.dist_to_gloms(tc_loc)
        closest_glom_idxs = np.argsort(glom_dists)

        closest_glom_loc = self.glom_locs[closest_glom_idxs][0]
        dist_to_closest_glom = glom_dists[closest_glom_idxs][0]

        longest_apic_reach = self.max_apic_tc_info["apical_dendrite_reach"]

        # Apics are too short - use the longest TC
        if dist_to_closest_glom > longest_apic_reach:
            base_class = self.max_apic_tc_info["class_name"]
            apic_glom_loc = closest_glom_loc

        # Apics are longer than distance
        else:
            # get tcs with apics longer than the closest glom,
            # but no further than ~200 um from glom (Kikuta et. al. 2013)
            longer_idxs = np.where((self.tc_apic_lengths > dist_to_closest_glom) &
                                   (np.array(self.tc_apic_lengths) - dist_to_closest_glom < 200))[0]

            # pick a random tc from this list
            rand_idx = longer_idxs[random.randrange(len(longer_idxs))]
            tc_apic_len = self.tc_apic_lengths[rand_idx]
            tc = list(self.tc_base_models.values())[rand_idx]

            # find a glom whose distance is as close to the length of the tc apic
            matching_glom_idx = np.argmin(np.abs(glom_dists - tc_apic_len))
            matching_glom_loc = self.glom_locs[matching_glom_idx]

            base_class = tc["class_name"]
            apic_glom_loc = matching_glom_loc


        # Create the selected TC in NRN
        instance_name = self.neuron.create_cell('TC', base_class)

        # Get updated list of NRN cells in Blender
        bpy.ops.custom.get_cell_list_from_neuron()

        # Select the created instance
        group = self.node.groups['Group.000']
        group.include_roots_by_name([instance_name], exclude_others=True)

        # Import group with the created cell
        bpy.ops.custom.import_selected_groups()

        tc_soma, tc_apic_start, tc_apic_end = \
            self.get_key_mctc_section_objects(self.tc_base_models, base_class, instance_name)

        # Align apical towards the closest glom
        self.position_orient_mctc(tc_soma,
                                  tc_apic_start,
                                  tc_apic_end,
                                  tc_loc,
                                  closest_glom_loc,
                                  apic_glom_loc)


        # Retain the reoriented cell
        bpy.ops.custom.update_groups_from_view()

        # Extend apic to the glom
        self.extend_apic(tc_apic_start, tc_apic_end, apic_glom_loc)

        self.align_dends(group, self.outer_opl_object_name)

        self.save_transform(instance_name, group)

    def add_gc(self, gc_loc):
        # find the closest glom loc
        inner_opl_dists = self.dist_to_opl(self.inner_opl_object_name, gc_loc)
        closest_iopl_idxs = np.argsort(inner_opl_dists)

        closest_glom_loc = self.inner_opl_locs[closest_iopl_idxs][0]
        dist_to_closest_glom = inner_opl_dists[closest_iopl_idxs][0]

        longest_apic_reach = self.max_apic_gc_info["apical_dendrite_reach"]

        # Apics are too short - use the longest GC
        if dist_to_closest_glom > longest_apic_reach:
            base_class = self.max_apic_gc_info["class_name"]
            apic_glom_loc = closest_glom_loc

        # Apics are longer than distance
        else:
            # get gcs with apics longer than the closest glom,
            # but no further than ~200 um from glom (Kikuta et. al. 2013)
            longer_idxs = np.where((self.tc_apic_lengths > dist_to_closest_glom) &
                                   (np.array(self.tc_apic_lengths) - dist_to_closest_glom < 200))[0]

            # pick a random tc from this list
            rand_idx = longer_idxs[random.randrange(len(longer_idxs))]
            tc_apic_len = self.tc_apic_lengths[rand_idx]
            tc = list(self.tc_base_models.values())[rand_idx]

            # find a glom whose distance is as close to the length of the tc apic
            matching_glom_idx = np.argmin(np.abs(inner_opl_dists - tc_apic_len))
            matching_glom_loc = self.glom_locs[matching_glom_idx]

            base_class = tc["class_name"]
            apic_glom_loc = matching_glom_loc


        # Create the selected TC in NRN
        instance_name = self.neuron.create_cell('TC', base_class)

        # Get updated list of NRN cells in Blender
        bpy.ops.custom.get_cell_list_from_neuron()

        # Select the created instance
        group = self.node.groups['Group.000']
        group.include_roots_by_name([instance_name], exclude_others=True)

        # Import group with the created cell
        bpy.ops.custom.import_selected_groups()

        tc_soma, tc_apic_start, tc_apic_end = \
            self.get_key_mctc_section_objects(self.tc_base_models, base_class, instance_name)

        # Align apical towards the closest glom
        self.position_orient_mctc(tc_soma,
                                  tc_apic_start,
                                  tc_apic_end,
                                  gc_loc,
                                  closest_glom_loc,
                                  apic_glom_loc)


        # Retain the reoriented cell
        bpy.ops.custom.update_groups_from_view()

        # Extend apic to the glom
        self.extend_apic(tc_apic_start, tc_apic_end, apic_glom_loc)

        self.align_dends(group, self.outer_opl_object_name)

        self.save_transform(instance_name, group)


    def align_dends(self, group, layer_name):
        # Set the layer
        group.set_layer(layer_name)

        # Setup the physics simulation
        group.setup_aligner()

        # Run the physics simulation (with progress visible)
        bpy.ops.ptcache.bake_all(bake=False)

    def save_transform(self, instance_name, group):

        # Make instance name a valid python module name (eg: MC1[0].soma -> MC1_0.py)
        file_name = instance_name \
                        .replace("].soma", "") \
                        .replace("[", "_") + \
                        ".py"

        # Save to slice folder
        path = os.path.join(self.slice_dir, file_name)

        # Save cells part of the group as files
        group.to_file(path)

    def get_key_mctc_section_objects(self, base_model_dict, base_class, instance_name):
        cell_info = base_model_dict[base_class]
        apic_pattern = instance_name.replace(".soma", "") + '.apic[%s]'

        bpy_objects = bpy.data.objects
        soma = bpy_objects[instance_name]
        apic_start = bpy_objects[apic_pattern % cell_info["apical_dendrite_start"]]
        apic_end = bpy_objects[apic_pattern % cell_info["apical_dendrite_end"]]

        return soma, apic_start, apic_end

    def get_longest_apic_model(self, base_model_dict):
        cell_names, apic_lengths = zip(*[(cell["class_name"], cell["apical_dendrite_reach"])
                                         for cell in base_model_dict.values()])

        max_apic_idx = np.argmax(apic_lengths)

        return base_model_dict[cell_names[max_apic_idx]]

    def dist_to_gloms(self, loc):
        return self.dist_to(self.glom_locs, loc)

    def dist_to_opl(self, opl_name, loc):
        opl = bpy.data.objects[opl_name]
        opl_pts = fast_get(opl.data.vertices, 'co', 3)
        return self.dist_to(opl_pts, loc)

    @staticmethod
    def dist_to(targets_array, loc):
        return np.sqrt(np.sum(np.square(targets_array - loc), axis=1))

    def get_locs_within_slice(self, particle_obj_name, slice_obj_name):
        particles = bpy.data.objects[particle_obj_name].particle_systems[0].particles
        slice_obj = bpy.data.objects[slice_obj_name]

        return np.array([np.array(ptc.location)
                         for ptc in particles
                         if self.is_inside(ptc.location, slice_obj)])

    def is_inside(self, point, obj):
        _, closest, normal, _ = obj.closest_point_on_mesh(point)
        p2 = closest - point
        v = p2.dot(normal)
        return not (v < 0.0)

    def unparent(self, obj):
        prev_parent = obj.parent
        parented_wm = obj.matrix_world.copy()
        obj.parent = None
        obj.matrix_world = parented_wm
        return prev_parent

    def parent(self, obj, parent):
        obj.parent = parent
        obj.matrix_parent_inverse = parent.matrix_world.inverted()

    def position_orient_mctc(self, soma, apic_start, apic_end, loc, closest_glom_loc, apic_glom_loc):

        # DEBUG aids
        bpy.data.objects['MCProbe'].location = loc
        bpy.data.objects['GlomProbe'].location = apic_glom_loc

        # Add random rotation around the apical axis
        soma.rotation_euler[2] = random.randrange(360) / 180.0 * pi

        # Position the soma
        soma.location = loc

        # Update child matrices
        bpy.context.scene.update()

        # Align the soma to be orthogonal to the soma-closest glom vector
        soma_wmi = soma.matrix_world.inverted()
        apic_end_loc = Vector(soma_wmi * apic_end.matrix_world * apic_end.location)
        glom_loc = Vector(soma_wmi * Vector(closest_glom_loc))

        initMW = soma.matrix_world.copy()
        rotM = apic_end_loc.rotation_difference(glom_loc).to_matrix().to_4x4()
        soma.matrix_world = initMW * rotM

        # Update child matrices
        bpy.context.scene.update()

        # Temporarily unparent the apic start (location becomes global)
        apic_start_parent = self.unparent(apic_start)
        apic_end_parent = self.unparent(apic_end)

        # Compute the start and end alignment vectors (start apic->end apic TO start apic->glom)
        # Relative to apic_start
        apic_start_wmi = apic_start.matrix_world.inverted()
        apic_end_loc = apic_start_wmi * apic_end.location

        startVec = Vector(apic_end_loc)
        endVec = Vector(apic_start_wmi * Vector(apic_glom_loc))

        # Reparent the apic end (so it rotates with the start apic)
        self.parent(apic_end, apic_end_parent)

        # Compute rotation quaternion and rotate the start apic by it
        initMW = apic_start.matrix_world.copy()
        rotM = startVec.rotation_difference(endVec).to_matrix().to_4x4()
        apic_start.matrix_world = initMW * rotM

        # Reparent the apic end (so it rotates with the start apic)
        self.parent(apic_start, apic_start_parent)

        bpy.context.scene.update()

    def extend_apic(self, apic_start, apic_end, apic_glom_loc):

        # Relative to apic_start
        glom_loc = apic_start.matrix_world.inverted() * Vector(apic_glom_loc)
        apic_end_loc = apic_start.matrix_world.inverted() * apic_end.matrix_world * apic_end.location

        apic_glom_diff = Vector(glom_loc - apic_end_loc)

        apic_start.location = apic_start.location.copy() + apic_glom_diff


bpy.app.handlers.scene_update_post.append(auto_start)