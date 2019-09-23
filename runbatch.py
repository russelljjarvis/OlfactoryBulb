import os

# paramsets = ['PureMCs',        'PureTCs']
# paramsets = ['PureMCsWithGJs', 'PureTCsWithGJs']

# paramsets = ['MCGJ_0', 'MCGJ_2', 'MCGJ_4', 'MCGJ_8', 'MCGJ_16', 'MCGJ_32',
#              'TCGJ_0', 'TCGJ_2', 'TCGJ_4', 'TCGJ_8', 'TCGJ_16', 'TCGJ_32']


# paramsets = ['MCsWithGJsGCs', 'TCsWithGJsGCs']

# paramsets = ['MCsWithGJsGCsExc_0', 'MCsWithGJsGCsExc_10', 'MCsWithGJsGCsExc_100', 'MCsWithGJsGCsExc_1000', 'MCsWithGJsGCsExc_10000',
#              'TCsWithGJsGCsExc_0', 'TCsWithGJsGCsExc_10', 'TCsWithGJsGCsExc_100', 'TCsWithGJsGCsExc_1000', 'TCsWithGJsGCsExc_10000',]


# paramsets = ['MCsWithGJsGCsInhib_0',
#                 'MCsWithGJsGCsInhib_1',
#                 'MCsWithGJsGCsInhib_2',
#                 'MCsWithGJsGCsInhib_4',
#                 'MCsWithGJsGCsInhib_8',
#
#                 'TCsWithGJsGCsInhib_0',
#                 'TCsWithGJsGCsInhib_1',
#                 'TCsWithGJsGCsInhib_2',
#                 'TCsWithGJsGCsInhib_4',
#                 'TCsWithGJsGCsInhib_8',]

# paramsets = [
#                 'MCsWithGJsGCsTau2_1',
#                 'MCsWithGJsGCsTau2_10',
#                 'MCsWithGJsGCsTau2_100',
#                 'MCsWithGJsGCsTau2_1000',
#
#
#                 'TCsWithGJsGCsTau2_1',
#                 'TCsWithGJsGCsTau2_10',
#                 'TCsWithGJsGCsTau2_100',
#                 'TCsWithGJsGCsTau2_1000',]

# paramsets = ['MC_TC_Combined_MC_weight_0',
#             'MC_TC_Combined_MC_weight_001',
#             'MC_TC_Combined_MC_weight_010',
#             'MC_TC_Combined_MC_weight_020',
#             'MC_TC_Combined_MC_weight_050',
#             'MC_TC_Combined_MC_weight_080',
#             'MC_TC_Combined_MC_weight_100',
#
#             'MC_TC_Combined_MC_delay_0',
#             'MC_TC_Combined_MC_delay_10',
#             'MC_TC_Combined_MC_delay_20',
#             'MC_TC_Combined_MC_delay_30',
#             'MC_TC_Combined_MC_delay_40',
#             'MC_TC_Combined_MC_delay_50',
#             'MC_TC_Combined_MC_delay_70',]


# paramsets = [
#     'MC_TC_Combined_MC_weight_0_delay_20',
#     'MC_TC_Combined_MC_weight_001_delay_20',
#     'MC_TC_Combined_MC_weight_010_delay_20',
#     'MC_TC_Combined_MC_weight_020_delay_20',
#     'MC_TC_Combined_MC_weight_050_delay_20',
#     'MC_TC_Combined_MC_weight_080_delay_20',
#     'MC_TC_Combined_MC_weight_100_delay_20',
#
#     'MC_TC_Combined_MC_weight_0_delay_30',
#     'MC_TC_Combined_MC_weight_001_delay_30',
#     'MC_TC_Combined_MC_weight_010_delay_30',
#     'MC_TC_Combined_MC_weight_020_delay_30',
#     'MC_TC_Combined_MC_weight_050_delay_30',
#     'MC_TC_Combined_MC_weight_080_delay_30',
#     'MC_TC_Combined_MC_weight_100_delay_30',
# ]


paramsets = [
    'TwoGammaClusters_InhibGmax_00',
    'TwoGammaClusters_InhibGmax_05',
    'TwoGammaClusters_InhibGmax_10',
    'TwoGammaClusters_InhibGmax_15',
    'TwoGammaClusters_InhibGmax_20',
    'TwoGammaClusters_InhibGmax_30'
]

for i, params in enumerate(paramsets):
    print('Starting paramset: ' + params + ' (%s/%s)...' % (i+1, len(paramsets)))
    os.system('mpiexec -np 16 python initslice.py -paramset '+params+' -mpi')
