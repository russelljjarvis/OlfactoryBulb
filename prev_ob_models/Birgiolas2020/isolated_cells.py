from prev_ob_models.utils import RunInClassDirectory, IsolatedCell
import os, sys

class MC(IsolatedCell):

    params = [
        {"start": 1, "attr": "diam", "low": 0.1, "high": 10.0, "lists": ["apical", "basal", "axonal"]},
        {"start": 34.77, "attr": "Ra", "low": 5.0, "high": 100.0, "lists": ["all"]},
        {"start": 2.706, "attr": "cm", "low": 0.1, "high": 4.0, "lists": ["all"]},
        {"start": 49.95, "attr": "ena", "low": 40.0, "high": 50.0, "lists": ["all"]},
        {"start": -70.03, "attr": "ek", "low": -100.0, "high": -70.0, "lists": ["all"]},
        {"start": -64.42, "attr": "e_pas", "low": -70.0, "high": -50.0, "lists": ["all"]},
        {"start": 0.0005955, "attr": "g_pas", "low": 0, "high": 0.00004, "lists": ["all"]},
        {"start": 0.5955, "attr": "sh_Na", "low": 0, "high": 10, "lists": ["all"]},
        {"start": 10, "attr": "tau_CaPool", "low": 1, "high": 20, "lists": ["all"]},

        {"start": 0.87485, "attr": "gbar_Na", "low": 0, "high": 0.05, "lists": ["all"]},
        {"start": 0.0297, "attr": "gbar_Kd", "low": 0, "high": 0.05, "lists": ["all"]},
        {"start": 0.000264, "attr": "gbar_Kslow", "low": 0, "high": 0.008, "lists": ["all"]},
        {"start": 0.07215, "attr": "gbar_KA", "low": 0, "high": 0.005, "lists": ["all"]},
        {"start": 0.001, "attr": "gbar_KCa", "low": 0, "high": 0.004, "lists": ["all"]},
        {"start": 0.00081441, "attr": "gbar_LCa", "low": 0, "high": 0.001, "lists": ["all"]},

        {"start": -30.805, "attr": "eh", "low": -40.0, "high": -25.0, "lists": ["apical"]},
        {"start": 0.00335, "attr": "gbar_Ih", "low": 0, "high": 0.000003, "lists": ["apical"]},
        {"start": 0.000107, "attr": "gbar_CaT", "low": 0, "high": 18e-3, "lists": ["apical"]},
    ]

    def __init__(self, mc_id):
        mc_id = str(mc_id)

        with RunInClassDirectory(MC):
            # Load the channels
            os.chdir("Mechanisms")
            from neuron import h#, gui
            os.chdir("..")

            h.load_file("stdrun.hoc")
            h.celsius = 35
            h.cvode_active(1)

            # Load the cell HOC file
            os.chdir("Cells")
            h.load_file("MC"+mc_id+".hoc")
            os.chdir("..")

            # Build the cell
            self.cell = getattr(h,"MC"+mc_id)()
            self.h = h
            self.soma = self.cell.soma



class MC1(MC):
    def __init__(self):
        super(MC1, self).__init__(mc_id=1)
        self.param_values = [1.5912202966117608, 12.795255635600554, 0.49637085627067434, 41.21596970666957, -76.74553376266104, -68.18994024980083, 3.7447764223294845e-05, 1.016335528899165, 5.95506515840653, 0.0049876210825029466, 0.008317122339242668, 0.0005572986108762616, 0.00067262699078494, 0.00015804600526572, 0.00010111601572365889, -39.87324758920763, 2.9829547341240183e-06, 0.0018294039520184967]
        self.set_model_params(self.param_values)

class MC2(MC):
    def __init__(self):
        super(MC2, self).__init__(mc_id=2)
        self.param_values = [1.5047867714566405, 28.436583720582952, 0.6998368828232051, 40.715749627373086, -74.44676547606643, -62.32883437747626, 3.920234942812064e-05, 0.517882120732251, 4.999948911797399, 0.00991222142319899, 0.014210196387989732, 0.0020620127761919824, 9.186217932936301e-06, 0.0029699814870417325, 8.095144873688063e-05, -26.811095685893473, 8.526117832793839e-07, 0.0018594503417942885]
        self.set_model_params(self.param_values)

class MC3(MC):
    def __init__(self):
        super(MC3, self).__init__(mc_id=3)
        self.param_values =  [0.9893784554721351, 7.155378518536821, 1.133918859861778, 40.85227476004934, -70.7015527367153, -54.35877091246093, 3.160299995152635e-05, 4.294619304296977, 15.346162579198172, 0.013340296827232938, 0.010783756546150481, 0.0007881919392502648, 0.0042509914069921466, 0.002743783625233259, 9.871561174152566e-05, -34.245440034960495, 1.8257881926835267e-06, 0.007501383229213064]
        self.set_model_params(self.param_values)

class MC4(MC):
    def __init__(self):
        super(MC4, self).__init__(mc_id=4)
        self.param_values = [2.2711969935973784, 32.390853224595084, 0.27358726967771324, 41.175796321038135, -71.43804177614685, -66.29008898509582, 8.293771372145503e-06, 1.0081749245859277, 1.7982090027418525, 0.02521909441159063, 0.015878223258567532, 0.0006262630523227793, 0.0009520859034589336, 0.003701980097991223, 5.3465646249391515e-05, -39.48930591931014, 8.217084060164491e-07, 0.00860947950944814]
        self.set_model_params(self.param_values)

class MC5(MC):
    def __init__(self):
        super(MC5, self).__init__(mc_id=5)
        self.param_values = [1.1216242855900833, 23.444749498570808, 1.050413118693083, 43.900489285737336, -70.72353749805104, -59.400443736342524, 3.089068326908354e-05, 4.307477215524907, 6.763621742215947, 0.012914278724257286, 0.01546316622188081, 0.0024267881019856617, 0.0021290100341655673, 0.0005191186351404533, 0.00018057535127379308, -35.48451294617036, 3.9082092036248225e-07, 0.005460273229467739]
        self.set_model_params(self.param_values)