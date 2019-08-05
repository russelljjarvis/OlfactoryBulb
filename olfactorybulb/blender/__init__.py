import bpy, sys, os
sys.path.append(os.getcwd())

from olfactorybulb.blender.slicebuilder import SliceBuilder

def auto_start(scene):

    # Remove auto-execute command after starting
    bpy.app.handlers.scene_update_post.remove(auto_start)

    # Assuming starting at repo root
    sys.path.append(os.getcwd())

    # Create a slice builder class
    bpy.types.Object.SliceBuilder = SliceBuilder()

bpy.app.handlers.scene_update_post.append(auto_start)

