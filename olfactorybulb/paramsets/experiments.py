from olfactorybulb.paramsets.case_studies import GammaSignature

# -------------- Delay --------------------- #
class GammaSignature_delay_0(GammaSignature):
    mc_input_delay = 0

class GammaSignature_delay_10(GammaSignature):
    mc_input_delay = 10

class GammaSignature_delay_20(GammaSignature):
    mc_input_delay = 20

class GammaSignature_delay_35(GammaSignature):
    mc_input_delay = 35

class GammaSignature_delay_40(GammaSignature):
    mc_input_delay = 40

class GammaSignature_delay_60(GammaSignature):
    mc_input_delay = 60



# -------------- MC Input Weight --------------------- #
class GammaSignature_MC_weight_0(GammaSignature):
    mc_input_weight = 0

class GammaSignature_MC_weight_025(GammaSignature):
    mc_input_weight = 0.25

class GammaSignature_MC_weight_050(GammaSignature):
    mc_input_weight = 0.50

class GammaSignature_MC_weight_075(GammaSignature):
    mc_input_weight = 0.75

class GammaSignature_MC_weight_100(GammaSignature):
    mc_input_weight = 1.0
