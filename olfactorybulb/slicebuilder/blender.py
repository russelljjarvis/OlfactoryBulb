import bpy, sys, os, time, re
import random
import os, sys
import bpy
import numpy as np
from collections import OrderedDict
from mathutils import Vector
import random
from math import pi, acos

sys.path.append(os.getcwd())
from olfactorybulb import slices
from blenderneuron.blender.utils import fast_get
from blenderneuron.blender.views.vectorconfinerview import VectorConfinerView
from blenderneuron.blender.views.synapseformerview import SynapseFormerView

'''
Sources:
Kikuta et. al. 2013 - TC soma distance from Glom center ~200 um
Witman and Greer 2007 - GC spine reach - from digitized figure 5.5 um
'''

def auto_start(scene):
    # Remove auto-execute command after starting
    bpy.app.handlers.scene_update_post.remove(auto_start)

    # Assuming starting at repo root
    sys.path.append(os.getcwd())

    # Create a slice builder class
    sbb = bpy.types.Object.SliceBuilder = SliceBuilderBlender()

    # from line_profiler import LineProfiler
    # lp = LineProfiler()
    # lp.add_function(sbb.add_mc)
    # lp.add_function(sbb.add_tc)
    # lp.add_function(sbb.add_gc)
    # lp.add_function(sbb.confine_dends)
    # lp.add_function(VectorConfinerView.confine_between_meshes)
    # profiled_build = lp(sbb.build)
    # profiled_build()
    # lp.print_stats()

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
                 odors=['Apple'], # use 'all' for all gloms, else e.g. ['Apple']
                 slice_object_name='TestSlice',
                 max_mcs=1, max_tcs=1, max_gcs=1,
                 mc_particles_object_name='2 ML Particles',
                 tc_particles_object_name='1 OPL Particles',
                 gc_particles_object_name='4 GRL Particles',
                 glom_particles_object_name='0 GL Particles',
                 glom_layer_object_name='0 GL',
                 outer_opl_object_name='1 OPL-Outer',
                 inner_opl_object_name='1 OPL-Inner'):

        self.odors = odors

        self.slice_name = slice_object_name

        self.max_mcs = max_mcs
        self.max_tcs = max_tcs
        self.max_gcs = max_gcs

        self.glom_particles_name = glom_particles_object_name
        self.tc_particles_name = tc_particles_object_name
        self.mc_particles_name = mc_particles_object_name
        self.gc_particles_name = gc_particles_object_name

        self.glom_layer_object_name = glom_layer_object_name
        self.outer_opl_object_name = outer_opl_object_name
        self.inner_opl_object_name = inner_opl_object_name

        # Within slice
        self.get_cell_locations()

        self.get_cell_base_model_info()

        # Show as section objects
        self.create_groups()

        # Add synapse sets
        self.add_synapse_sets()

        # Clear slice files
        self.clear_slice_files()

        self.max_alignment_angle = 15

    def build(self, seed=0):
        random.seed(seed)

        for loc in self.mc_locs:
            self.add_mc(loc)

        for loc in self.tc_locs:
            self.add_tc(loc)

        for loc in self.gc_locs:
            self.add_gc(loc)

        # Select all cells in groups
        self.node.groups['MCs'].select_roots('Pattern','MC*')
        self.node.groups['TCs'].select_roots('Pattern','TC*')
        self.node.groups['GCs'].select_roots('Pattern','GC*')

        # Show all group cells
        bpy.ops.blenderneuron.display_groups()

    def add_synapse_sets(self):
        # Delete the default set
        self.node.synapse_sets.remove(0)

        self.create_synapse_set('GCs', 'MCs')
        self.create_synapse_set('GCs', 'TCs')

    def create_synapse_set(self, group_from, group_to):

        new_set = self.node.add_synapse_set(group_from + '->' + group_to)
        new_set.group_source = group_from
        new_set.group_dest = group_to

        new_set.max_distance = 5
        new_set.use_radius = True
        new_set.max_syns_per_pt = 1
        new_set.section_pattern_source = "*apic*"
        new_set.section_pattern_dest = "*dend*"
        new_set.synapse_name_dest = 'GabaSyn'
        new_set.synapse_params_dest = str({
            'gmax': 0.005,  # uS,
            'tau1': 1,  # ms
            'tau2': 100  # ms
        })
        new_set.is_reciprocal = True
        new_set.synapse_name_source = 'AmpaNmdaSyn'
        new_set.synapse_params_source = str({'gmax': 0.1})
        new_set.create_spines = True
        new_set.spine_neck_diameter = 0.2
        new_set.spine_head_diameter = 1
        new_set.spine_name_prefix = 'Spine'
        new_set.conduction_velocity = 1
        new_set.initial_weight = 1
        new_set.threshold = 0

    def clear_slice_files(self):
        dir = self.slice_dir

        # Match e.g. 'MC1_21.py'
        pattern = re.compile('.C.+_.+py')

        for file in os.listdir(dir):
            if pattern.match(file) is not None:
                os.remove(os.path.abspath(os.path.join(dir, file)))

    def get_cell_locations(self):
        self.globalize_slice()

        odor_glom_ids = self.neuron.get_odor_gloms(self.odors)
        self.glom_locs = self.get_locs_within_slice(self.glom_particles_name, self.slice_name, odor_glom_ids)

        self.inner_opl_locs = self.get_opl_locs(self.inner_opl_object_name, self.slice_name)
        self.outer_opl_locs = self.get_opl_locs(self.outer_opl_object_name, self.slice_name)

        self.mc_locs = self.get_locs_within_slice(self.mc_particles_name, self.slice_name)[:self.max_mcs]
        self.tc_locs = self.get_locs_within_slice(self.tc_particles_name, self.slice_name)[:self.max_tcs]
        self.gc_locs = self.get_locs_within_slice(self.gc_particles_name, self.slice_name)[:self.max_gcs]

        print('Gloms:', len(self.glom_locs))
        print('TCs:', len(self.tc_locs))
        print('MCs:', len(self.mc_locs))
        print('GCs:', len(self.gc_locs))

    def get_opl_locs(self, opl_name, slice_obj_name):

        obj = bpy.data.objects[opl_name]
        wm = obj.matrix_world

        locs = fast_get(obj.data.vertices, 'co', 3)

        def globalize(loc):
            return np.array(wm * Vector(loc))

        # Globalize the coordinates
        locs = np.array(list(map(globalize, locs)))

        slice_obj = bpy.data.objects[slice_obj_name]

        return np.array([pt
                         for pt in locs
                         if self.is_inside(Vector(pt), slice_obj)])

    def get_cell_base_model_info(self):
        self.mc_base_models, self.tc_base_models, self.gc_base_models = \
            self.neuron.get_base_model_info()

        self.mc_base_models = OrderedDict(sorted(self.mc_base_models.items(), key=lambda i: i[0]))
        self.tc_base_models = OrderedDict(sorted(self.tc_base_models.items(), key=lambda i: i[0]))
        self.gc_base_models = OrderedDict(sorted(self.gc_base_models.items(), key=lambda i: i[0]))

        self.max_apic_mc_info = self.get_longest_apic_model(self.mc_base_models)
        self.mc_apic_lengths = self.get_apic_lengths(self.mc_base_models)

        self.max_apic_tc_info = self.get_longest_apic_model(self.tc_base_models)
        self.tc_apic_lengths = self.get_apic_lengths(self.tc_base_models)

        self.max_apic_gc_info = self.get_longest_apic_model(self.gc_base_models)
        self.gc_apic_lengths = self.get_apic_lengths(self.gc_base_models)

    @staticmethod
    def get_apic_lengths(base_models):
        return np.array([tc["apical_dendrite_reach"] for tc in base_models.values()])

    def create_groups(self):
        # Remove the default group
        self.node.groups['Group.000'].remove()

        # Create empty cell groups
        groups = [self.node.add_group(name, False) for name in ['MCs', 'TCs', 'GCs']]

        # show each section as blender objects - necessary for dend alignment
        for group in groups:
            group.interaction_granularity = 'Section'
            group.recording_granularity = 'Cell'
            group.record_activity = False

        group[1].default_color = [1, 0, 0]
        group[2].default_color = [0, 0, 1]

    def globalize_slice(self):
        # Apply all/any transformations to the slice
        slice = bpy.data.objects[self.slice_name]
        slice.select = True
        bpy.context.scene.objects.active = slice
        bpy.ops.object.transform_apply(location=True, scale=True, rotation=True)
        slice.select = False

    def add_mc(self, mc_pt):

        # find the closest glom layer loc - cell will be pointed towards it
        closest_glom_loc, dist_to_gl = \
            self.closest_point_on_object(mc_pt['loc'], bpy.data.objects[self.glom_layer_object_name])

        longest_apic_reach = self.max_apic_mc_info["apical_dendrite_reach"]

        # Apics are too short - skip the location
        if dist_to_gl > longest_apic_reach:
            return

        # get mcs with apics longer than dist to GL
        longer_idxs = np.where(self.mc_apic_lengths > dist_to_gl)[0]

        # pick a random mc from this list
        mc = self.get_random_model(self.mc_base_models, longer_idxs)

        # find a glom whose distance is as close to the length of the mc apic
        matching_glom_loc = self.find_matching_glom(mc_pt['loc'], mc)

        base_class = mc["class_name"]
        apic_glom_loc = matching_glom_loc

        # Create the selected MC in NRN
        instance_name = self.neuron.create_cell('MC', base_class)

        # Import it into Blender
        self.import_instance(instance_name, 'MCs')

        mc_soma, mc_apic_start, mc_apic_end = \
            self.get_key_mctc_section_objects(self.mc_base_models, base_class, instance_name)

        # Align apical towards the closest glom
        self.position_orient_align_mctc(mc_soma,
                                        mc_apic_start,
                                        mc_apic_end,
                                        mc_pt['loc'],
                                        closest_glom_loc,
                                        apic_glom_loc)

        # Retain the reoriented cell
        bpy.ops.blenderneuron.update_groups_with_view_data()

        # self.confine_dends(
        #     'MCs',
        #     self.inner_opl_object_name,
        #     self.outer_opl_object_name,
        #     max_angle=self.max_alignment_angle,
        #     height_start=0,
        #     height_end=0.6
        # )
        #
        # self.save_transform('MCs', instance_name)

    def import_instance(self, instance_name, group_name):
        # Get updated list of NRN cells in Blender
        bpy.ops.blenderneuron.get_cell_list_from_neuron()

        # Select the created instance
        group = self.node.groups[group_name]
        group.include_roots_by_name([instance_name], exclude_others=True)

        # Import group with the created cell and show it
        group.import_group()
        group.show()

    def add_tc(self, tc_pt):

        # find the closest glom layer loc - cell will be pointed towards it
        closest_glom_loc, dist_to_gl = \
            self.closest_point_on_object(tc_pt['loc'], bpy.data.objects[self.glom_layer_object_name])

        longest_apic_reach = self.max_apic_tc_info["apical_dendrite_reach"]

        # Apics are too short - leave that location blank
        if dist_to_gl > longest_apic_reach:
            return

        # Apics are longer than distance
        # get tcs with apics longer than the closest glom,
        # but no further than ~200 um from glom (Source: Kikuta et. al. 2013)
        longer_idxs = np.where((self.tc_apic_lengths > dist_to_gl) &
                               (self.tc_apic_lengths - dist_to_gl < 200))[0]

        # pick a random tc from this list
        tc = self.get_random_model(self.tc_base_models, longer_idxs)

        # find a glom whose distance is as close to the length of the tc apic
        matching_glom_loc = self.find_matching_glom(tc_pt['loc'], tc)

        base_class = tc["class_name"]
        apic_glom_loc = matching_glom_loc

        # Create the selected TC in NRN
        instance_name = self.neuron.create_cell('TC', base_class)

        # Import it into Blender
        self.import_instance(instance_name, 'TCs')

        soma, apic_start, apic_end = \
            self.get_key_mctc_section_objects(self.tc_base_models, base_class, instance_name)

        # Align apical towards the closest glom
        self.position_orient_align_mctc(soma,
                                        apic_start,
                                        apic_end,
                                        tc_pt['loc'],
                                        closest_glom_loc,
                                        apic_glom_loc)

        # Retain the reoriented cell
        bpy.ops.blenderneuron.update_groups_with_view_data()

        self.confine_dends(
            'TCs',
            self.inner_opl_object_name,
            self.outer_opl_object_name,
            max_angle=self.max_alignment_angle,
            height_start=0.4,
            height_end=1.0
        )

        self.save_transform('TCs', instance_name)

    def find_matching_glom(self, cell_loc, cell_model_info):
        # Get distances to individual gloms
        glom_dists = self.dist_to_gloms(cell_loc)

        matching_glom_idx = np.argmin(np.abs(glom_dists - cell_model_info["apical_dendrite_reach"]))
        matching_glom_loc = self.glom_locs[matching_glom_idx]['loc']
        return matching_glom_loc

    def get_opl_distance_info(self, cell_loc, pts):
        dists = self.dist_to(pts, cell_loc)
        closest_idxs = np.argsort(dists)

        closest_loc = pts[closest_idxs][0]
        closest_dist = dists[closest_idxs][0]

        return closest_loc, closest_dist, dists

    @staticmethod
    def closest_point_on_object(global_pt, mesh_obj):
        local_pt = mesh_obj.matrix_world.inverted() * Vector(global_pt)

        _, mesh_pt, _, _ = mesh_obj.closest_point_on_mesh(local_pt)

        mesh_pt_global = mesh_obj.matrix_world * mesh_pt

        dist = Vector(global_pt - mesh_pt_global).length

        return np.array(mesh_pt_global), dist

    def add_gc(self, gc_pt):

        # find the closest glom loc - cell will be pointed towards it
        glom_loc, glom_dist = \
            self.closest_point_on_object(gc_pt['loc'], bpy.data.objects[self.glom_layer_object_name])

        # find the closest inner opl loc - apics must go beyond this
        closest_iopl_loc, dist_to_iopl = \
            self.closest_point_on_object(gc_pt['loc'], bpy.data.objects[self.inner_opl_object_name])

        # find the closest outer opl loc - apics must stay under this
        closest_oopl_loc, dist_to_oopl = \
            self.closest_point_on_object(gc_pt['loc'], bpy.data.objects[self.outer_opl_object_name])

        longest_apic_reach = self.max_apic_gc_info["apical_dendrite_reach"]

        # If apics are longer than distance, find such GC models whose apics are confined to the OPL
        # Specifically:
        # Get gcs with apics 30um or more longer than the closest opl
        # GCs whose dendrites penetrate less than ~this amount into OPL would be
        # functionally inert (in this model)
        # AND
        # the apic does not exceed outer opl + margin
        min_length = dist_to_iopl + 30
        max_length = dist_to_oopl + 30

        matching_idxs = np.where((self.gc_apic_lengths > min_length) &
                                 (self.gc_apic_lengths < max_length))[0]

        # If no cell can reach IOPL, leave that location blank
        if len(matching_idxs) == 0:
            return

        # pick a random gc from this list
        gc = self.get_random_model(self.gc_base_models, matching_idxs)

        base_class = gc["class_name"]
        apic_opl_loc = closest_iopl_loc

        # Create the selected GC in NRN
        instance_name = self.neuron.create_cell('GC', base_class)

        # Import it into Blender
        self.import_instance(instance_name, 'GCs')

        soma, apic_start, apic_end = \
            self.get_key_mctc_section_objects(self.gc_base_models, base_class, instance_name)

        self.position_orient_cell(soma, apic_end, gc_pt['loc'], apic_opl_loc)

        # Retain the reoriented cell
        bpy.ops.blenderneuron.update_groups_with_view_data()

        self.save_transform('GCs', instance_name)

    def get_random_model(self, base_models, longer_idxs):
        rand_idx = longer_idxs[random.randrange(len(longer_idxs))]
        cell = list(base_models.values())[rand_idx]
        return cell

    def confine_dends(self, group_name, start_layer_name, end_layer_name, max_angle, height_start, height_end):
        group = self.node.groups[group_name]

        # Set the layers
        group.set_confiner_layers(start_layer_name, end_layer_name, max_angle, height_start, height_end)
        group.setup_confiner()
        group.confine_between_layers()

    def save_transform(self, group_name, instance_name):

        group = self.node.groups[group_name]

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

        apic_start = bpy_objects.get(apic_pattern % cell_info["apical_dendrite_start"])
        apic_end = bpy_objects.get(apic_pattern % cell_info["apical_dendrite_end"])

        return soma, apic_start, apic_end

    def get_longest_apic_model(self, base_model_dict):
        cell_names, apic_lengths = zip(*[(cell["class_name"], cell["apical_dendrite_reach"])
                                         for cell in base_model_dict.values()])

        max_apic_idx = np.argmax(apic_lengths)

        return base_model_dict[cell_names[max_apic_idx]]

    def dist_to_gloms(self, loc):
        return self.dist_to(np.array([glom['loc'] for glom in self.glom_locs]), loc)

    @staticmethod
    def dist_to(targets_array, loc):
        return np.sqrt(np.sum(np.square(targets_array - loc), axis=1))

    def get_locs_within_slice(self, particle_obj_name, slice_obj_name, allowed_particles=None):
        particles_obj = bpy.data.objects[particle_obj_name]
        particles = particles_obj.particle_systems[0].particles
        particles_wm = particles_obj.matrix_world
        slice_obj = bpy.data.objects[slice_obj_name]

        result = [{ 'id': pid, 'loc': np.array(particles_wm * ptc.location)}
                           for pid, ptc in enumerate(particles)
                           if (allowed_particles is None or pid in allowed_particles) and
                           self.is_inside(particles_wm * ptc.location, slice_obj)]

        return result

    @staticmethod
    def is_inside(target_pt_global, mesh_obj, tolerance=0.05):
        # Convert the point from global space to mesh local space
        target_pt_local = mesh_obj.matrix_world.inverted() * target_pt_global

        # Find the nearest point on the mesh and the nearest face normal
        _, pt_closest, face_normal, _ = mesh_obj.closest_point_on_mesh(target_pt_local)

        # Get the target-closest pt vector
        target_closest_pt_vec = (pt_closest - target_pt_local).normalized()

        # Compute the dot product = |a||b|*cos(angle)
        dot_prod = target_closest_pt_vec.dot(face_normal)

        # Get the angle between the normal and the target-closest-pt vector (from the dot prod)
        angle = acos(min(max(dot_prod, -1), 1)) * 180 / pi

        # Allow for some rounding error
        inside = angle < 90 - tolerance

        return inside

    def unparent(self, obj):
        prev_parent = obj.parent
        parented_wm = obj.matrix_world.copy()
        obj.parent = None
        obj.matrix_world = parented_wm
        return prev_parent

    def parent(self, obj, parent):
        obj.parent = parent
        obj.matrix_parent_inverse = parent.matrix_world.inverted()

    def position_orient_align_mctc(self, soma, apic_start, apic_end, loc, closest_glom_loc, apic_glom_loc):

        self.position_orient_cell(soma, apic_end, loc, closest_glom_loc)

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

    def position_orient_cell(self, soma, apic_end, soma_loc, closest_glom_loc):
        # Add random rotation around the apical axis
        soma.rotation_euler[2] = random.randrange(360) / 180.0 * pi

        # Position the soma
        soma.location = soma_loc

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

    def extend_apic(self, apic_start, apic_end, apic_glom_loc):

        # Relative to apic_start
        glom_loc = apic_start.matrix_world.inverted() * Vector(apic_glom_loc)
        apic_end_loc = apic_start.matrix_world.inverted() * apic_end.matrix_world * apic_end.location

        apic_glom_diff = Vector(glom_loc - apic_end_loc)

        apic_start.location = apic_start.location.copy() + apic_glom_diff




bpy.app.handlers.scene_update_post.append(auto_start)
