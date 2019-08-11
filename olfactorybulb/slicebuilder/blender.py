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
                 max_mcs=0, max_tcs=5, max_gcs=0,
                 mc_particles_object_name='2 ML Particles',
                 tc_particles_object_name='1 OPL Particles',
                 gc_particles_object_name='4 GRL Particles',
                 glom_particles_object_name='0 GL Particles',
                 glom_layer_object_name='0 GL',
                 outer_opl_object_name='1 OPL-Outer',
                 inner_opl_object_name='1 OPL-Inner'):

        random.seed(0)

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
        self.globalize_slice()

        self.glom_locs = self.get_locs_within_slice(self.glom_particles_name, self.slice_name)

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

        self.mc_base_models = OrderedDict(self.mc_base_models)
        self.tc_base_models = OrderedDict(self.tc_base_models)
        self.gc_base_models = OrderedDict(self.gc_base_models)

        self.max_apic_mc_info = self.get_longest_apic_model(self.mc_base_models)
        self.mc_apic_lengths = self.get_apic_lengths(self.mc_base_models)

        self.max_apic_tc_info = self.get_longest_apic_model(self.tc_base_models)
        self.tc_apic_lengths = self.get_apic_lengths(self.tc_base_models)

        self.max_apic_gc_info = self.get_longest_apic_model(self.gc_base_models)
        self.gc_apic_lengths = self.get_apic_lengths(self.gc_base_models)

    @staticmethod
    def get_apic_lengths(base_models):
        return np.array([tc["apical_dendrite_reach"] for tc in base_models.values()])

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
            mc = self.get_random_model(self.mc_base_models, longer_idxs)

            # find a glom whose distance is as close to the length of the mc apic
            matching_glom_loc = self.find_matching_glom(loc, mc)

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
        self.position_orient_align_mctc(mc_soma,
                                        mc_apic_start,
                                        mc_apic_end,
                                        loc,
                                        closest_glom_loc,
                                        apic_glom_loc)


        # Retain the reoriented cell
        bpy.ops.custom.update_groups_from_view()

        # Extend apic to the glom
        # self.extend_apic(mc_apic_start, mc_apic_end, apic_glom_loc)

        #self.align_dends(group, self.inner_opl_object_name)

        self.save_transform(instance_name, group)

    def add_tc(self, loc):

        # find the closest glom layer loc - cell will be pointed towards it
        closest_glom_loc, dist_to_gl = \
            self.closest_point_on_object(loc, bpy.data.objects[self.glom_layer_object_name])

        longest_apic_reach = self.max_apic_tc_info["apical_dendrite_reach"]

        # Apics are too short - leave that location blank
        if dist_to_gl > longest_apic_reach:
            return

        # Apics are longer than distance
        # get tcs with apics longer than the closest glom,
        # but no further than ~200 um from glom (Kikuta et. al. 2013)
        longer_idxs = np.where((self.tc_apic_lengths > dist_to_gl) &
                               (self.tc_apic_lengths - dist_to_gl < 200))[0]

        # pick a random tc from this list
        tc = self.get_random_model(self.tc_base_models, longer_idxs)

        # find a glom whose distance is as close to the length of the tc apic
        matching_glom_loc = self.find_matching_glom(loc, tc)

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

        soma, apic_start, apic_end = \
            self.get_key_mctc_section_objects(self.tc_base_models, base_class, instance_name)

        # Align apical towards the closest glom
        self.position_orient_align_mctc(soma,
                                        apic_start,
                                        apic_end,
                                        loc,
                                        closest_glom_loc,
                                        apic_glom_loc)


        # Retain the reoriented cell
        bpy.ops.custom.update_groups_from_view()

        # Extend apic to the glom
        # self.extend_apic(tc_apic_start, tc_apic_end, apic_glom_loc)

        #self.align_dends(group, self.outer_opl_object_name)

        self.save_transform(instance_name, group)

    def find_matching_glom(self, cell_loc, cell_model_info):
        # Get distances to individual gloms
        glom_dists = self.dist_to_gloms(cell_loc)

        matching_glom_idx = np.argmin(np.abs(glom_dists - cell_model_info["apical_dendrite_reach"]))
        matching_glom_loc = self.glom_locs[matching_glom_idx]
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

    def add_gc(self, loc):

        # find the closest glom loc - cell will be pointed towards it
        glom_loc, glom_dist = \
            self.closest_point_on_object(loc, bpy.data.objects[self.glom_layer_object_name])

        # find the closest inner opl loc - apics must go beyond this
        closest_iopl_loc, dist_to_iopl = \
            self.closest_point_on_object(loc, bpy.data.objects[self.inner_opl_object_name])

        # find the closest outer opl loc - apics must stay under this
        closest_oopl_loc, dist_to_oopl = \
            self.closest_point_on_object(loc, bpy.data.objects[self.outer_opl_object_name])

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

        # Get updated list of NRN cells in Blender
        bpy.ops.custom.get_cell_list_from_neuron()

        # Select the created instance
        group = self.node.groups['Group.000']
        group.include_roots_by_name([instance_name], exclude_others=True)

        # Import group with the created cell
        bpy.ops.custom.import_selected_groups()

        soma, apic_start, apic_end = \
            self.get_key_mctc_section_objects(self.gc_base_models, base_class, instance_name)

        # DEBUG aids
        bpy.data.objects['MCProbe'].location = loc
        bpy.data.objects['GlomProbe'].location = apic_opl_loc

        self.position_orient_cell(soma, apic_end, loc, apic_opl_loc)

        # Retain the reoriented cell
        bpy.ops.custom.update_groups_from_view()

        self.save_transform(instance_name, group)

    def get_random_model(self, base_models, longer_idxs):
        rand_idx = longer_idxs[random.randrange(len(longer_idxs))]
        cell = list(base_models.values())[rand_idx]
        return cell

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

        apic_start = bpy_objects.get(apic_pattern % cell_info["apical_dendrite_start"])
        apic_end = bpy_objects.get(apic_pattern % cell_info["apical_dendrite_end"])

        return soma, apic_start, apic_end

    def get_longest_apic_model(self, base_model_dict):
        cell_names, apic_lengths = zip(*[(cell["class_name"], cell["apical_dendrite_reach"])
                                         for cell in base_model_dict.values()])

        max_apic_idx = np.argmax(apic_lengths)

        return base_model_dict[cell_names[max_apic_idx]]

    def dist_to_gloms(self, loc):
        return self.dist_to(self.glom_locs, loc)

    @staticmethod
    def dist_to(targets_array, loc):
        return np.sqrt(np.sum(np.square(targets_array - loc), axis=1))

    def get_locs_within_slice(self, particle_obj_name, slice_obj_name):
        particles_obj = bpy.data.objects[particle_obj_name]
        particles = particles_obj.particle_systems[0].particles
        particles_wm = particles_obj.matrix_world
        slice_obj = bpy.data.objects[slice_obj_name]

        result = np.array([np.array(particles_wm * ptc.location)
                           for ptc in particles
                           if self.is_inside(particles_wm * ptc.location, slice_obj)])

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
        inside = angle < 90-tolerance

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

        # DEBUG aids
        bpy.data.objects['MCProbe'].location = loc
        bpy.data.objects['GlomProbe'].location = apic_glom_loc

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