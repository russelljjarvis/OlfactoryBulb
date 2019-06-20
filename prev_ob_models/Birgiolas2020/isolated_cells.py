from prev_ob_models.utils import RunInClassDirectory, IsolatedCell
import os, sys

class OlfactoryBulbCell(IsolatedCell):
    def __init__(self, cell_id):
        cell_id = str(cell_id)

        with RunInClassDirectory(OlfactoryBulbCell):
            # Load the channels
            os.chdir("Mechanisms")
            from neuron import h, gui
            os.chdir("..")

            h.load_file("stdrun.hoc")
            h.celsius = 35
            h.cvode_active(1)

            # Load the cell HOC file (they follow MC1.hoc, GC1.hoc, ... pattern)
            os.chdir("Cells")
            h.load_file(self.cell_type + cell_id + ".hoc")
            os.chdir("..")

            # Build the cell
            self.cell = getattr(h,self.cell_type + cell_id)()
            self.h = h
            self.soma = self.cell.soma

class MC(OlfactoryBulbCell):

    # Parameters and their ranges used for fitting
    params = [
        {"start": 1, "attr": "diam", "low": 0.1, "high": 5.0, "lists": ["apical", "basal", "axonal"]},
        {"start": 34.77, "attr": "Ra", "low": 1.0, "high": 150.0, "lists": ["all"]},
        {"start": 2.706, "attr": "cm", "low": 0.1, "high": 2.0, "lists": ["all"]},
        {"start": 49.95, "attr": "ena", "low": 20.0, "high": 50.0, "lists": ["all"]},
        {"start": -70.03, "attr": "ek", "low": -100.0, "high": -50.0, "lists": ["all"]},
        {"start": -64.42, "attr": "e_pas", "low": -90.0, "high": -50.0, "lists": ["all"]},
        {"start": 0.0005955, "attr": "g_pas", "low": 0, "high": 0.00004, "lists": ["all"]},
        {"start": 0.5955, "attr": "sh_Na", "low": 0, "high": 10, "lists": ["all"]},
        {"start": 10, "attr": "tau_CaPool", "low": 1, "high": 10, "lists": ["all"]},

        {"start": 0.87485, "attr": "gbar_Na", "low": 0, "high": 0.05, "lists": ["all"]},
        {"start": 0.0297, "attr": "gbar_Kd", "low": 0, "high": 0.05, "lists": ["all"]},
        {"start": 0.000264, "attr": "gbar_Kslow", "low": 0, "high": 0.001, "lists": ["all"]},
        {"start": 0.07215, "attr": "gbar_KA", "low": 0, "high": 0.01, "lists": ["all"]},
        {"start": 0.001, "attr": "gbar_KCa", "low": 0, "high": 0.004, "lists": ["all"]},
        {"start": 0.00081441, "attr": "gbar_LCa", "low": 0, "high": 0.0005, "lists": ["all"]},

        {"start": -30.805, "attr": "eh", "low": -40.0, "high": -15.0, "lists": ["apical"]},
        {"start": 0.00335, "attr": "gbar_Ih", "low": 0, "high": 0.000001, "lists": ["apical"]},
        {"start": 0.000107, "attr": "gbar_CaT", "low": 0, "high": 10e-3, "lists": ["apical"]},
    ]

    cell_type = "MC"


class MC1(MC):
    def __init__(self):
        super(MC1, self).__init__(cell_id=1)
        # self.param_values = [4.483822127802881, 8.66219433612183, 0.8924323616844085, 22.781408934638648, -71.36528075596314, -68.12595932359295, 3.6318149288201166e-05, 1.5349502819878742, 9.731038623592067, 0.045200023063995017, 0.037639185681536326, 0.000539438090733542, 0.008199477373572574, 0.0018205696406990688, 0.00043444216625588845, -32.66490045884105, 3.9928550864601285e-07, 0.005060526438354798]
        # self.set_model_params(self.param_values)

class MC2(MC):
    def __init__(self):
        super(MC2, self).__init__(cell_id=2)
        self.param_values = [0.3613335821366068, 30.420919689411967, 0.29378161070335246, 39.67851249768874, -69.6017843681071, -89.92170626820798, 1.0981245439095467e-05, 7.560335627779654, 4.890021485515521, 0.010009317760275055, 0.009218587409873507, 0.0002565337724007733, 9.361526427683915e-05, 0.0035722983493425, 0.00013356700530123668, -22.396316115635408, 5.749441391501133e-08, 0.002557222666817198]
        self.set_model_params(self.param_values)

class MC3(MC):
    def __init__(self):
        super(MC3, self).__init__(cell_id=3)
        self.param_values =  [1.4120455494333222, 20.772715084585002, 0.1629078628574005, 25.136347200545135, -69.61305911117856, -88.23178536958522, 6.172695057662258e-07, 7.2396164215691625, 8.73252611645168, 0.018466467372100746, 0.035976302714844914, 6.762360967648025e-06, 0.0033650755298665876, 0.0036211383303654085, 7.69402377321008e-05, -25.314057520795465, 1.5882522346200823e-07, 0.008158155610703025]
        self.set_model_params(self.param_values)

class MC4(MC):
    def __init__(self):
        super(MC4, self).__init__(cell_id=4)
        self.param_values = [0.15632786941738305, 6.772518501265802, 0.6206949249072544, 31.687376571673248, -77.02945694714829, -87.4045787617848, 2.4749631379932633e-05, 7.093280595111089, 3.636068593365941, 0.029434352712679468, 0.037262189460739364, 0.00010836576354121376, 0.0005885331207977784, 0.0006157269510378659, 0.0004752601735862538, -17.973032345752323, 3.8191481893937475e-07, 0.0038685549465372524]
        self.set_model_params(self.param_values)

class MC5(MC):
    def __init__(self):
        super(MC5, self).__init__(cell_id=5)
        self.param_values = [0.34905155854489744, 17.625178998796677, 0.47035755820670444, 38.077668587244055, -81.64426601866356, -81.61472207521145, 1.4392462997513291e-05, 6.183378879538829, 4.650077244029179, 0.010376753988263012, 0.012787761114543742, 5.93053166793121e-06, 1.2373036719639372e-05, 0.0038805851999001327, 2.0404661784841133e-06, -23.814770114099073, 9.464530701606e-08, 0.003746506966633768]
        self.set_model_params(self.param_values)


class GC(OlfactoryBulbCell):

    # Parameters and their ranges used for fitting
    params = [
        { "attr": "diam",  "low": 0.1, "high": 3.0, "lists": ["apical"]},

        { "attr": "Ra",    "low": 5.0, "high": 20.0, "lists": ["all"]},
        { "attr": "cm",    "low": 0.1, "high": 4.0, "lists": ["all"]},
        { "attr": "ena",   "low": 10.0, "high": 50.0, "lists": ["all"]},
        { "attr": "ek",    "low": -100.0, "high": -30.0, "lists": ["all"]},
        { "attr": "e_pas", "low": -100.0, "high": -50.0, "lists": ["all"]},
        { "attr": "g_pas", "low": 0, "high": 0.0002, "lists": ["all"]},
        { "attr": "sh_Na", "low": 0, "high": 10, "lists": ["all"]},
        { "attr": "gbar_Na", "low": 0, "high": 0.05, "lists": ["all"]},
        { "attr": "gbar_Kd", "low": 0, "high": 0.1, "lists": ["all"]},

        { "attr": "gbar_KA", "low": 0, "high": 0.01, "lists": ["somatic"]},
        { "attr": "eh",      "low": -50.0, "high": -15.0, "lists": ["somatic"]},
        { "attr": "gbar_Ih", "low": 0, "high": 0.000001, "lists": ["somatic"]},
        { "attr": "gbar_KM", "low": 0, "high": 0.13, "lists": ["somatic"]},

    ]

    cell_type = "GC"

class GC1(GC):
    def __init__(self):
        super(GC1, self).__init__(cell_id=1)
        self.param_values = [0.936025277676213, 6.129869170282754, 0.555853926533468, 30.29798502856093, -56.57531217196064, -88.97736796138885, 3.560099788534217e-05, 4.371318574477207, 0.010523028908442221, 0.03610398043715232, 0.00015534929542823875, -39.09938496951048, 7.115016182590743e-08, 0.025013201684461608]
        self.set_model_params(self.param_values)

class GC2(GC):
    def __init__(self):
        super(GC2, self).__init__(cell_id=1)
        self.param_values = [1.2933074765569572, 15.964921848533345, 0.6209279330160213, 24.833205129696545, -81.5462724857123, -89.47831949412408, 3.670390933276994e-05, 3.302314197046086, 0.012922940997028532, 0.025154533917713457, 0.0020329731062468234, -47.374038053028265, 4.352344991619022e-07, 0.024231291210945503]
        self.set_model_params(self.param_values)

class GC3(GC):
    def __init__(self):
        super(GC3, self).__init__(cell_id=1)
        self.param_values = [1.0165229591551166, 8.742223695142892, 1.3325653588637776, 39.55645462323818, -54.418207489400096, -85.55338135654503, 6.320847994173219e-05, 2.779506490030582, 0.01794877469106408, 0.03540413668753805, 0.003160423997086609, -29.116485041419523, 2.6361301968714977e-07, 0.04200071666187057]
        self.set_model_params(self.param_values)

class GC4(GC):
    def __init__(self):
        super(GC4, self).__init__(cell_id=1)
        self.param_values = [0.9025324638516083, 8.753031686148644, 0.9380308731945421, 46.213018519563214, -52.35792469538774, -87.9408887746017, 5.283149360026259e-05, 4.956645884463499, 0.01012695819079385, 0.02205488674836242, 0.0034793106167388304, -26.786851403254495, 6.0673504219961e-07, 0.04718614854337389]
        self.set_model_params(self.param_values)

class GC5(GC):
    def __init__(self):
        super(GC5, self).__init__(cell_id=1)
        self.param_values = [0.9376348175328878, 11.591714654531046, 1.0324034688967776, 28.54236760189409, -84.25400415668759, -86.38671125769042, 5.576876711838849e-05, 0.6815923359096576, 0.015906079474993826, 0.06193378170794706, 0.000692474429499574, -40.074832002660145, 2.888298777423034e-07, 0.005007473558389143]
        self.set_model_params(self.param_values)