"""
This file is used to sequentially run the network model using different sets of parameters
"""

import os

paramsets = [
    # "GammaSignature_GJ_0",
    # "GammaSignature_GJ_1",
    # "GammaSignature_GJ_2",
    # "GammaSignature_GJ_4",
    # "GammaSignature_GJ_8",
    # "GammaSignature_GJ_16",
    # "GammaSignature_GJ_32",
    # "GammaSignature_GJ_64",
    # "GammaSignature_GJ_128",
    #
    # "GammaSignature_AMPANMDA_0",
    # "GammaSignature_AMPANMDA_1",
    # "GammaSignature_AMPANMDA_2",
    # "GammaSignature_AMPANMDA_4",
    # "GammaSignature_AMPANMDA_8",
    # "GammaSignature_AMPANMDA_16",
    # "GammaSignature_AMPANMDA_32",
    # "GammaSignature_AMPANMDA_64",
    # "GammaSignature_AMPANMDA_128",
    # "GammaSignature_AMPANMDA_256",

    "GammaSignature_GABA_0",
    "GammaSignature_GABA_1",
    "GammaSignature_GABA_2",
    "GammaSignature_GABA_4",
    "GammaSignature_GABA_8",

    "GammaSignature_TCWGHT_00",
    "GammaSignature_TCWGHT_02",
    "GammaSignature_TCWGHT_04",
    "GammaSignature_TCWGHT_06",
    "GammaSignature_TCWGHT_08",
    "GammaSignature_TCWGHT_10",


    "GammaSignature_MCWGHT_00",
    "GammaSignature_MCWGHT_02",
    "GammaSignature_MCWGHT_04",
    "GammaSignature_MCWGHT_06",
    "GammaSignature_MCWGHT_08",
    "GammaSignature_MCWGHT_10",

]


for i, params in enumerate(paramsets):
    print('Starting paramset: ' + params + ' (%s/%s)...' % (i+1, len(paramsets)))
    os.system('mpiexec -np 16 python initslice.py -paramset '+params+' -mpi')
