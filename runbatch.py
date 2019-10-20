import os

# Compute isolated MCs or TCs and effect of GJ conductance on each
paramsets = [ 'PureMCs', 'PureTCs',
             'MCGJ_0', 'MCGJ_2', 'MCGJ_4', 'MCGJ_8', 'MCGJ_16', 'MCGJ_32',
             'TCGJ_0', 'TCGJ_2', 'TCGJ_4', 'TCGJ_8', 'TCGJ_16', 'TCGJ_32']

# Select GJ conductance and then add GC inhibition
paramsets = ['PureMCsWithGJs', 'PureTCsWithGJs']

# Explore effect of exciting GCs by either MCs or TCs
paramsets = ['MCsWithGJsGCsExc_0', 'MCsWithGJsGCsExc_10', 'MCsWithGJsGCsExc_100', 'MCsWithGJsGCsExc_1000', 'MCsWithGJsGCsExc_10000',
             'TCsWithGJsGCsExc_0', 'TCsWithGJsGCsExc_10', 'TCsWithGJsGCsExc_100', 'TCsWithGJsGCsExc_1000', 'TCsWithGJsGCsExc_10000',]

# Explore effect of inhibition of MCs or TCs
paramsets = ['MCsWithGJsGCsInhib_0',
                'MCsWithGJsGCsInhib_1',
                'MCsWithGJsGCsInhib_2',
                'MCsWithGJsGCsInhib_4',
                'MCsWithGJsGCsInhib_8',

                'TCsWithGJsGCsInhib_0',
                'TCsWithGJsGCsInhib_1',
                'TCsWithGJsGCsInhib_2',
                'TCsWithGJsGCsInhib_4',
                'TCsWithGJsGCsInhib_8',]

# Explore effect of inhibitory time constant
paramsets = [
                'MCsWithGJsGCsTau2_1',
                'MCsWithGJsGCsTau2_10',
                'MCsWithGJsGCsTau2_50',
                'MCsWithGJsGCsTau2_100',
                'MCsWithGJsGCsTau2_500',
                'MCsWithGJsGCsTau2_1000',


                'TCsWithGJsGCsTau2_1',
                'TCsWithGJsGCsTau2_10',
                'TCsWithGJsGCsTau2_50',
                'TCsWithGJsGCsTau2_100',
                'TCsWithGJsGCsTau2_500',
                'TCsWithGJsGCsTau2_1000',]



# Select exc and inhibit gmax and taus
paramsets = ['MCsWithGJsGCs', 'TCsWithGJsGCs']

# Combine MC and TC network and explore effect of MC input weight and delay
paramsets = [   'MC_TC_Combined_MC_weight_025_delay_20',
                'MC_TC_Combined_MC_weight_050_delay_20',
                'MC_TC_Combined_MC_weight_075_delay_20',

                'MC_TC_Combined_MC_weight_025_delay_30',
                'MC_TC_Combined_MC_weight_050_delay_30',
                'MC_TC_Combined_MC_weight_075_delay_30',

                'MC_TC_Combined_MC_weight_025_delay_40',
                'MC_TC_Combined_MC_weight_050_delay_40',
                'MC_TC_Combined_MC_weight_075_delay_40',]



# # Select MC delay and weight
# paramsets = ['GammaSignature']

# # Effect of mc delay
# paramsets = [
#     # 'GammaSignature_delay_0',
#     # 'GammaSignature_delay_10',
#     # 'GammaSignature_delay_20',
#     # 'GammaSignature_delay_35',
#     'GammaSignature_delay_40',
#     'GammaSignature_delay_60',
# ]

# # Effect of MC input weight
# paramsets = [
#     'GammaSignature_MC_weight_0',
#     'GammaSignature_MC_weight_025',
#     'GammaSignature_MC_weight_050',
#     'GammaSignature_MC_weight_075',
#     'GammaSignature_MC_weight_100',
# ]


for i, params in enumerate(paramsets):
    print('Starting paramset: ' + params + ' (%s/%s)...' % (i+1, len(paramsets)))
    os.system('mpiexec -np 16 python initslice.py -paramset '+params+' -mpi')
