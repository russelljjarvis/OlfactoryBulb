from prev_ob_models.utils import RunInClassDirectory, IsolatedCell
import os, sys

class OlfactoryBulbCell(IsolatedCell):
    def __init__(self, cell_id):
        self.cell_id = str(cell_id)

        with RunInClassDirectory(OlfactoryBulbCell):
            # Load the channels
            os.chdir("Mechanisms")
            from neuron import h#, gui
            os.chdir("..")

            h.load_file("stdrun.hoc")
            h.celsius = 35
            h.cvode_active(1)

            # Load the cell HOC file (they follow MC1.hoc, GC1.hoc, ... pattern)
            os.chdir("Cells")
            self.hoc_path = os.path.abspath(self.cell_type + str(cell_id) + ".hoc")
            h.load_file(self.hoc_path)
            os.chdir("..")

            # Build the cell
            self.hoc_template = self.cell_type + str(cell_id)
            self.cell = getattr(h, self.hoc_template)()
            self.h = h
            self.soma = self.cell.soma

    def set_model_params(self, param_values):
        from neuron import h

        # The diam param functions as a scaling factor of the existing diameters
        # to be able to set the params multiple times, the original diams need to be used when multiplying
        # Here, this is done by instantiating an unmodified copy of the cell
        unmodified_cell = getattr(h, self.hoc_template)()

        for pi, pv in enumerate(param_values):
            attr = self.params[pi]["attr"]
            if attr == "tau_CaPool":
                setattr(h, attr, pv)
            else:
                for param_list in self.params[pi]["lists"]:
                    if attr == "diam":
                        unmodified_secs = [sec for sec in getattr(unmodified_cell, param_list)]

                    for isec, sec in enumerate(getattr(self.cell, param_list)):
                        if attr == "diam":
                            for i3d in range(int(h.n3d(sec=sec))):
                                orig_diam = h.diam3d(i3d, sec=unmodified_secs[isec])
                                h.pt3dchange(i3d, orig_diam * pv, sec=sec)
                        else:
                            setattr(sec, attr, pv)

        del unmodified_cell

class MC(OlfactoryBulbCell):

    # Parameters and their ranges used for fitting
    params = [
        {"start": 1, "attr": "diam", "low": 0.1, "high": 5.0, "lists": ["apical", "basal", "axonal"]},
        {"start": 34.77, "attr": "Ra", "low": 1.0, "high": 150.0, "lists": ["all"]},
        {"start": 2.706, "attr": "cm", "low": 0.1, "high": 2.0, "lists": ["all"]},
        {"start": 49.95, "attr": "ena", "low": 20.0, "high": 80.0, "lists": ["all"]},
        {"start": -70.03, "attr": "ek", "low": -100.0, "high": -50.0, "lists": ["all"]},
        {"start": -64.42, "attr": "e_pas", "low": -90.0, "high": -50.0, "lists": ["all"]},
        {"start": 0.0005955, "attr": "g_pas", "low": 0, "high": 0.00004, "lists": ["all"]},
        {"start": 0.5955, "attr": "sh_Na", "low": 0, "high": 10, "lists": ["all"]},
        {"start": 10, "attr": "tau_CaPool", "low": 1, "high": 300, "lists": ["all"]},

        {"start": 0.87485, "attr": "gbar_Na", "low": 0, "high": 0.1, "lists": ["all"]},
        {"start": 0.0297, "attr": "gbar_Kd", "low": 0, "high": 0.1, "lists": ["all"]},
        {"start": 0.000264, "attr": "gbar_Kslow", "low": 0, "high": 0.001, "lists": ["all"]},
        {"start": 0.07215, "attr": "gbar_KA", "low": 0, "high": 0.02, "lists": ["all"]},
        {"start": 0.001, "attr": "gbar_KCa", "low": 0, "high": 0.016, "lists": ["all"]},
        {"start": 0.00081441, "attr": "gbar_LCa", "low": 0, "high": 0.0005, "lists": ["all"]},

        {"start": -30.805, "attr": "eh", "low": -40.0, "high": -10.0, "lists": ["apical"]},
        {"start": 0.00335, "attr": "gbar_Ih", "low": 0, "high": 0.000003, "lists": ["apical"]},
        {"start": 0.000107, "attr": "gbar_CaT", "low": 0, "high": 20e-3, "lists": ["apical"]},
    ]

    cell_type = "MC"


class MC1(MC):
    def __init__(self):
        super(MC1, self).__init__(cell_id=1)
        self.param_values = [3.22389443491247, 2.81865928031078, 0.33261043003167834, 27.0037817821923, -64.93732914068036, -73.25204775921887, 2.1361316231147274e-05, 3.76535811520783, 4.308024855943862, 0.03186952629227804, 0.023795201285494796, 0.0007185750073984963, 0.002526117846022963, 0.0009455163544555489, 0.00016863361902873404, -36.099624268474926, 3.655648607819723e-07, 0.004428920251185234]
        self.set_model_params(self.param_values)

class MC2(MC):
    def __init__(self):
        super(MC2, self).__init__(cell_id=2)
        self.param_values = [2.3511459438710984,126.79240156883097,0.5169516132656169,36.70146443789503,-59.939258607150514,-63.44102868866163,2.508982638071978e-05,3.4858670343332308,7.507321595674958,0.013630971923446833,0.0011455738584287012,0.00038998349958084864,0.003250159154661294,0.0037771563959725,0.0004433261041866151,-15.91046573495657,1.816124175620452e-07,0.007912495290042867]
        self.set_model_params(self.param_values)

class MC3(MC):
    def __init__(self):
        super(MC3, self).__init__(cell_id=3)
        self.param_values =  [2.5423168283445956, 22.24438742171681, 0.6495059435075267, 25.514798622627445, -69.80712920166272, -57.42040781764916, 1.9476222649318898e-05, 4.343600147915433, 6.659410081345059, 0.04428811469036931, 0.014229735150034572, 0.0001648293604053363, 0.005382990776749325, 0.0012568660047021492, 0.00010974581311243848, -28.970056925719366, 6.455001190237628e-07, 0.002468829827979082]
        self.set_model_params(self.param_values)

class MC4(MC):
    def __init__(self):
        super(MC4, self).__init__(cell_id=4)
        self.param_values = [1.0882827660647931, 8.97791641084582, 0.6307453448260578, 44.81115966615397, -61.19341314098865, -72.77205927215527, 3.0005066359112136e-05, 1.2273167760473112, 8.57738871414464, 0.009745103588705815, 0.016814274105780822, 0.0008630161891010214, 0.0029899442463640303, 0.0017233830355042575, 0.0003758675164563642, -20.101758455718468, 9.699711091593169e-07, 0.0011559009225374898]
        self.set_model_params(self.param_values)

class MC5(MC):
    def __init__(self):
        super(MC5, self).__init__(cell_id=5)
        self.param_values = [1.2471592703753913, 89.54731666051053, 0.9576321104748539, 23.163661456098886, -63.438841110533915, -75.05751351034053, 3.657331273597089e-05, 2.6570771987427655, 9.666857483589407, 0.06150916169169841, 0.03759175148995797, 0.0004759847063037054, 0.0042226776511213, 0.00776370232830789, 9.599737738463663e-06, -16.369883529143777, 1.9500130790130927e-06, 0.01027446638931233]
        self.set_model_params(self.param_values)


class GC(OlfactoryBulbCell):

    # Parameters and their ranges used for fitting
    params = [
        { "attr": "diam",  "low": 0.1, "high": 3.0, "lists": ["apical"]},

        { "attr": "Ra",    "low": 5.0, "high": 120.0, "lists": ["all"]},
        { "attr": "cm",    "low": 0.1, "high": 4.0, "lists": ["all"]},
        { "attr": "ena",   "low": 10.0, "high": 50.0, "lists": ["all"]},
        { "attr": "ek",    "low": -100.0, "high": -30.0, "lists": ["all"]},
        { "attr": "e_pas", "low": -100.0, "high": -50.0, "lists": ["all"]},
        { "attr": "g_pas", "low": 0, "high": 0.0002, "lists": ["all"]},
        { "attr": "sh_Na", "low": 0, "high": 10, "lists": ["all"]},
        { "attr": "gbar_Na", "low": 0, "high": 0.1, "lists": ["all"]},
        { "attr": "gbar_Kd", "low": 0, "high": 0.1, "lists": ["all"]},

        { "attr": "gbar_KA", "low": 0, "high": 0.02, "lists": ["somatic"]},
        { "attr": "eh",      "low": -50.0, "high": -10.0, "lists": ["somatic"]},
        { "attr": "gbar_Ih", "low": 0, "high": 0.000004, "lists": ["somatic"]},
        { "attr": "gbar_KM", "low": 0, "high": 0.13, "lists": ["somatic"]},

    ]

    cell_type = "GC"

class GC1(GC):
    def __init__(self):
        super(GC1, self).__init__(cell_id=1)
        self.param_values = [0.9025324638516083, 8.753031686148644, 0.9380308731945421, 46.213018519563214, -52.35792469538774, -87.9408887746017, 5.283149360026259e-05, 4.956645884463499, 0.01012695819079385, 0.02205488674836242, 0.0034793106167388304, -26.786851403254495, 6.0673504219961e-07, 0.04718614854337389]
        self.set_model_params(self.param_values)

class GC2(GC):
    def __init__(self):
        super(GC2, self).__init__(cell_id=2)
        self.param_values = [0.8710267875973179, 14.641561962581802, 1.297028578568163, 23.542384925570374, -66.14931267317124, -86.9860149734769, 7.372686439889864e-05, 9.015897486544564, 0.0663024552362425, 0.08054323387277286, 0.009253490640782557, -42.24621117356369, 2.416646001483452e-06, 0.0027768216611947063]
        self.set_model_params(self.param_values)

class GC3(GC):
    def __init__(self):
        super(GC3, self).__init__(cell_id=3)
        # self.param_values = [1.0165229591551166, 8.742223695142892, 1.3325653588637776, 39.55645462323818, -54.418207489400096, -85.55338135654503, 6.320847994173219e-05, 2.779506490030582, 0.01794877469106408, 0.03540413668753805, 0.003160423997086609, -29.116485041419523, 2.6361301968714977e-07, 0.04200071666187057]
        # self.set_model_params(self.param_values)

class GC4(GC):
    def __init__(self):
        super(GC4, self).__init__(cell_id=4)
        # self.param_values = [0.9025324638516083, 8.753031686148644, 0.9380308731945421, 46.213018519563214, -52.35792469538774, -87.9408887746017, 5.283149360026259e-05, 4.956645884463499, 0.01012695819079385, 0.02205488674836242, 0.0034793106167388304, -26.786851403254495, 6.0673504219961e-07, 0.04718614854337389]
        # self.set_model_params(self.param_values)

class GC5(GC):
    def __init__(self):
        super(GC5, self).__init__(cell_id=5)
        # self.param_values = [0.9376348175328878, 11.591714654531046, 1.0324034688967776, 28.54236760189409, -84.25400415668759, -86.38671125769042, 5.576876711838849e-05, 0.6815923359096576, 0.015906079474993826, 0.06193378170794706, 0.000692474429499574, -40.074832002660145, 2.888298777423034e-07, 0.005007473558389143]
        # self.set_model_params(self.param_values)
        
        
        
class TC(OlfactoryBulbCell):

    # Parameters and their ranges used for fitting
    params = [
        {"start": 1, "attr": "diam", "low": 0.1, "high": 5.0, "lists": ["apical", "basal", "axonal"]},
        {"start": 34.77, "attr": "Ra", "low": 1.0, "high": 150.0, "lists": ["all"]},
        {"start": 2.706, "attr": "cm", "low": 0.1, "high": 2.0, "lists": ["all"]},
        {"start": 49.95, "attr": "ena", "low": 20.0, "high": 80.0, "lists": ["all"]},
        {"start": -70.03, "attr": "ek", "low": -100.0, "high": -50.0, "lists": ["all"]},
        {"start": -64.42, "attr": "e_pas", "low": -90.0, "high": -50.0, "lists": ["all"]},
        {"start": 0.0005955, "attr": "g_pas", "low": 0, "high": 0.00004, "lists": ["all"]},
        {"start": 0.5955, "attr": "sh_Na", "low": 0, "high": 10, "lists": ["all"]},
        {"start": 10, "attr": "tau_CaPool", "low": 1, "high": 300, "lists": ["all"]},

        {"start": 0.87485, "attr": "gbar_Na", "low": 0, "high": 0.1, "lists": ["all"]},
        {"start": 0.0297, "attr": "gbar_Kd", "low": 0, "high": 0.1, "lists": ["all"]},
        {"start": 0.000264, "attr": "gbar_Kslow", "low": 0, "high": 0.001, "lists": ["all"]},
        {"start": 0.07215, "attr": "gbar_KA", "low": 0, "high": 0.02, "lists": ["all"]},
        {"start": 0.001, "attr": "gbar_KCa", "low": 0, "high": 0.016, "lists": ["all"]},
        {"start": 0.00081441, "attr": "gbar_LCa", "low": 0, "high": 0.0010, "lists": ["all"]},

        {"start": -30.805, "attr": "eh", "low": -40.0, "high": -10.0, "lists": ["apical"]},
        {"start": 0.00335, "attr": "gbar_Ih", "low": 0, "high": 0.000003, "lists": ["apical"]},
        {"start": 0.000107, "attr": "gbar_CaT", "low": 0, "high": 20e-3, "lists": ["apical"]},
    ]

    cell_type = "TC"


class TC1(TC):
    def __init__(self):
        super(TC1, self).__init__(cell_id=1)
        #self.param_values = [3.22389443491247, 2.81865928031078, 0.33261043003167834, 27.0037817821923, -64.93732914068036, -73.25204775921887, 2.1361316231147274e-05, 3.76535811520783, 4.308024855943862, 0.03186952629227804, 0.023795201285494796, 0.0007185750073984963, 0.002526117846022963, 0.0009455163544555489, 0.00016863361902873404, -36.099624268474926, 3.655648607819723e-07, 0.004428920251185234]
        #self.set_model_params(self.param_values)

class TC2(TC):
    def __init__(self):
        super(TC2, self).__init__(cell_id=2)
        #self.param_values = [2.3511459438710984,126.79240156883097,0.5169516132656169,36.70146443789503,-59.939258607150514,-63.44102868866163,2.508982638071978e-05,3.4858670343332308,7.507321595674958,0.013630971923446833,0.0011455738584287012,0.00038998349958084864,0.003250159154661294,0.0037771563959725,0.0004433261041866151,-15.91046573495657,1.816124175620452e-07,0.007912495290042867]
        #self.set_model_params(self.param_values)

class TC3(TC):
    def __init__(self):
        super(TC3, self).__init__(cell_id=3)
        #self.param_values =  [2.5423168283445956, 22.24438742171681, 0.6495059435075267, 25.514798622627445, -69.80712920166272, -57.42040781764916, 1.9476222649318898e-05, 4.343600147915433, 6.659410081345059, 0.04428811469036931, 0.014229735150034572, 0.0001648293604053363, 0.005382990776749325, 0.0012568660047021492, 0.00010974581311243848, -28.970056925719366, 6.455001190237628e-07, 0.002468829827979082]
        #self.set_model_params(self.param_values)

class TC4(TC):
    def __init__(self):
        super(TC4, self).__init__(cell_id=4)
        #self.param_values = [1.0882827660647931, 8.97791641084582, 0.6307453448260578, 44.81115966615397, -61.19341314098865, -72.77205927215527, 3.0005066359112136e-05, 1.2273167760473112, 8.57738871414464, 0.009745103588705815, 0.016814274105780822, 0.0008630161891010214, 0.0029899442463640303, 0.0017233830355042575, 0.0003758675164563642, -20.101758455718468, 9.699711091593169e-07, 0.0011559009225374898]
        #self.set_model_params(self.param_values)

class TC5(TC):
    def __init__(self):
        super(TC5, self).__init__(cell_id=5)
        #self.param_values = [1.2471592703753913, 89.54731666051053, 0.9576321104748539, 23.163661456098886, -63.438841110533915, -75.05751351034053, 3.657331273597089e-05, 2.6570771987427655, 9.666857483589407, 0.06150916169169841, 0.03759175148995797, 0.0004759847063037054, 0.0042226776511213, 0.00776370232830789, 9.599737738463663e-06, -16.369883529143777, 1.9500130790130927e-06, 0.01027446638931233]
        #self.set_model_params(self.param_values)