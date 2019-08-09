# Most of the work is performed in Blender
# Here we start NRN, add some helper methods that can be called from Blender
# Then start Blender+addon and let it build the slice model

import sys, os
from olfactorybulb.slicebuilder.nrn import SliceBuilderNRN

# Start NRN and the addon
sbn = SliceBuilderNRN()

# Start Blender and build the model
os.system("blender blender-files/ob-gloms-fast.blend --python olfactorybulb/slicebuilder/blender.py")