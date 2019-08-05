"""
Want to be able to select a slice from db or from blender file
Then using the blender file layers, slice, and particle information, build the model by
positioning, orienting, aligning cells, saving their positions

then need to connect them

question is how do I load large scripts into blender that I could call when needed
pass a param?
"""

# Load blender file

# Connect to blender

import random
import os, sys
import bpy
import numpy as np
from collections import OrderedDict


class SliceBuilder:
    @property
    def node(self):
        return bpy.types.Object.BlenderNEURON_node

    @property
    def neuron(self):
        return self.node.client

    def __init__(self,
                 slice_object_name='TestSlice',
                 mc_particles_object_name='2 ML Particles',
                 tc_particles_object_name='1 OPL Particles',
                 gc_particles_object_name='4 GRL Particles',
                 glom_particles_object_name='0 GL Particles',
                 outer_opl_object_name='1 OPL.001',
                 inner_opl_object_name='1 OPL.002'):

        random.seed(0)

        self.slice_name = slice_object_name

        self.glom_particles_name = glom_particles_object_name
        self.tc_particles_name = tc_particles_object_name
        self.mc_particles_name = mc_particles_object_name
        self.gc_particles_name = gc_particles_object_name

        self.outer_opl_object_name = outer_opl_object_name
        self.inner_opl_object_name = inner_opl_object_name

        import pydevd
        pydevd.settrace('192.168.0.100', port=4200)

        # Within slice
        self.get_cell_locations()

        self.get_cell_base_model_info()

        # Show as section objects
        self.prepare_group()

    def get_cell_locations(self):
        slice = bpy.data.objects[self.slice_name]

        self.globalize_slice()

        self.mc_locs = self.get_locs_within_slice(self.mc_particles_name, self.slice_name)
        self.glom_locs = self.get_locs_within_slice(self.glom_particles_name, self.slice_name)
        #self.tc_locs = self.get_locs_within_slice(self.tc_particles_name, self.slice_name)
        #self.gc_locs = self.get_locs_within_slice(self.gc_particles_name, self.slice_name)

        print('Gloms:', len(self.glom_locs))
        # print('TCs:', len(self.tc_locs))
        print('MCs:', len(self.mc_locs))
        # print('GCs:', len(self.gc_locs))

    def get_cell_base_model_info(self):
        self.mc_base_models, self.tc_base_models, self.gc_base_models = \
            self.neuron.get_base_model_info()

        self.mc_base_models = OrderedDict(self.mc_base_models)
        self.tc_base_models = OrderedDict(self.tc_base_models)
        self.gc_base_models = OrderedDict(self.gc_base_models)

        self.max_apic_mc_info = self.get_longest_apic_mc()
        self.mc_apic_lengths = [mc["apical_dendrite_reach"] for mc in self.mc_base_models.values()]

    def prepare_group(self):
        # show each section as blender objects
        group = self.node.groups['Group.000']
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
        for mc_loc in self.mc_locs:
            self.add_mc(mc_loc)

        self.add_tcs()
        self.add_gcs()

    def add_mc(self, mc_loc):

        # find the closest glom loc
        glom_dists = self.dist_to_gloms(mc_loc)
        closest_glom_idxs = np.argsort(glom_dists)

        closest_glom = self.glom_locs[closest_glom_idxs][0]
        dist_to_closest_glom = glom_dists[closest_glom_idxs][0]

        longest_apic_reach = self.max_apic_mc_info["apical_dendrite_reach"]

        # Apics are too short - use the longest MC
        if dist_to_closest_glom > longest_apic_reach:
            base_class = self.max_apic_mc_info["class_name"]
            glom_loc = closest_glom

        # Apics are longer than distance
        else:
            # get mcs with apics longer than the closest glom
            longer_idxs = np.where(self.mc_apic_lengths > dist_to_closest_glom)[0]

            # pick a random mc from this list
            rand_idx = longer_idxs[random.randrange(len(longer_idxs))]
            mc_apic_len = self.mc_apic_lengths[rand_idx]
            mc = self.mc_base_models.keys()[rand_idx]

            # find a glom whose distance is as close to the length of the mc apic
            matching_glom_idx = np.argmin(np.abs(glom_dists - mc_apic_len))
            matching_glom_loc = self.glom_locs[matching_glom_idx]

            base_class = mc["class_name"]
            glom_loc = matching_glom_loc

        # Create the selected MC in NRN
        instance_name = self.neuron.create_mc(base_class)

        # Get updated list of NRN cells in Blender
        bpy.ops.custom.get_cell_list_from_neuron()

        # Select the created instance
        group = self.node.groups['Group.000']
        group.include_roots_by_name([instance_name], exclude_others=True)

        # Import group with the created cell
        bpy.ops.custom.import_selected_groups()

        mc_soma, mc_apic_start, mc_apic_end = \
            self.get_key_mc_section_objects(base_class, instance_name)

        # Align apical towards the closest glom
        self.position_orient_mc(mc_soma,
                                mc_apic_start,
                                mc_apic_end,
                                mc_loc,
                                glom_loc)

        #     # Extend apic to the glom
        #     self.extend_apic(mc_apic_end, mc_info["mc_loc"], mc_info["glom_loc"])

        self.align_dends(group, self.inner_opl_object_name)

        self.save_transform(instance_name, group)

    def add_tcs(self):
        pass

    def add_gcs(self):
        pass

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
        from olfactorybulb import slices
        slice_dir = os.path.abspath(os.path.dirname(slices.__file__))
        path = os.path.join(slice_dir, self.slice_name, file_name)

        # Save cells part of the group as a file
        group.to_file(path)

    def get_key_mc_section_objects(self, base_class, instance_name):
        mc_info = self.mc_base_models[base_class]
        apic_pattern = instance_name.replace(".soma", "") + '.apic[%s]'

        bpy_objects = bpy.data.objects
        mc_soma = bpy_objects[instance_name]
        mc_apic_start = bpy_objects[apic_pattern % mc_info["apical_dendrite_start"]]
        mc_apic_end = bpy_objects[apic_pattern % mc_info["apical_dendrite_end"]]

        return mc_soma, mc_apic_start, mc_apic_end

    def get_longest_apic_mc(self):
        mc_names, mc_apic_lengths = zip(*[(mc["class_name"], mc["apical_dendrite_reach"])
                                          for mc in self.mc_base_models.values()])

        max_apic_idx = np.argmax(mc_apic_lengths)

        return self.mc_base_models[mc_names[max_apic_idx]]

    def dist_to_gloms(self, loc):
        return np.sqrt(np.sum(np.square(self.glom_locs - loc), axis=1))

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

    def position_orient_mc(self, soma, apic_start, apic_end, loc, glom_loc):
        from mathutils import Vector
        import random
        from math import pi

        # DEBUG aids
        bpy.data.objects['MCProbe'].location = loc
        bpy.data.objects['GlomProbe'].location = glom_loc

        # Add random rotation around the apical axis
        soma.rotation_euler[2] = random.randrange(360) / 180.0 * pi

        # Position the soma
        soma.location = loc

        # Update child matrices
        bpy.context.scene.update()

        # Temporarily unparent the apic start (location becomes global)
        apic_start_parent = self.unparent(apic_start)
        apic_end_parent = self.unparent(apic_end)

        # Compute the start and end alignment vectors (start apic->end apic TO start apic->glom)
        # Relative to apic_start
        apic_start_wmi = apic_start.matrix_world.inverted()
        apic_start_loc = apic_start_wmi * apic_start.location  # Can be 0,0,0?
        apic_end_loc = apic_start_wmi * apic_end.location

        startVec = Vector(apic_end_loc - apic_start_loc)
        endVec = Vector(apic_start_wmi * Vector(glom_loc) - apic_start_loc)

        # Reparent the apic end (so it rotates with the start apic)
        self.parent(apic_end, apic_end_parent)

        # Compute rotation quaternion and rotate the start apic by it
        initMW = apic_start.matrix_world.copy()
        rotM = startVec.rotation_difference(endVec).to_matrix().to_4x4()
        apic_start.matrix_world = initMW * rotM

        # Reparent the apic end (so it rotates with the start apic)
        self.parent(apic_start, apic_start_parent)

        bpy.context.scene.update()

    def extend_apic(self, apic_end, apic_start_loc, glom_loc):
        from mathutils import Vector

        apic_end_loc = apic_end.location.copy()
        apic_vec = Vector(apic_end_loc - apic_start_loc)

        dist_to_end = Vector(glom_loc - apic_end_loc).length
        dist_ratio = dist_to_end / apic_vec.length

        apic_end.location = apic_vec * dist_ratio
