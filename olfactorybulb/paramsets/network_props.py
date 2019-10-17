from olfactorybulb.paramsets.case_studies import *

# delay 20, 30, 40
# weight 0.25, 0.5, 0.75

class MC_TC_Combined_MC_weight_025_delay_20(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.25
    mc_input_delay = 20

class MC_TC_Combined_MC_weight_050_delay_20(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.50
    mc_input_delay = 20

class MC_TC_Combined_MC_weight_075_delay_20(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.75
    mc_input_delay = 20

class MC_TC_Combined_MC_weight_025_delay_30(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.25
    mc_input_delay = 30

class MC_TC_Combined_MC_weight_050_delay_30(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.50
    mc_input_delay = 30

class MC_TC_Combined_MC_weight_075_delay_30(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.75
    mc_input_delay = 30

class MC_TC_Combined_MC_weight_025_delay_40(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.25
    mc_input_delay = 40

class MC_TC_Combined_MC_weight_050_delay_40(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.50
    mc_input_delay = 40

class MC_TC_Combined_MC_weight_075_delay_40(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.75
    mc_input_delay = 40


# Effect of Gaba gmax on TCMC clusters #
class GammaSignature_InhibGmax_00(GammaSignature):

    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 500,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        },

        "GabaSyn": {
            'gmax': 0,
            'tau2': 100,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        }
    }

class GammaSignature_InhibGmax_05(GammaSignature):

    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 500,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        },

        "GabaSyn": {
            'gmax': 0.5,
            'tau2': 100,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        }
    }

class GammaSignature_InhibGmax_10(GammaSignature):

    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 500,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        },

        "GabaSyn": {
            'gmax': 1,
            'tau2': 100,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        }
    }

class GammaSignature_InhibGmax_15(GammaSignature):

    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 500,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        },

        "GabaSyn": {
            'gmax': 1.5,
            'tau2': 100,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        }
    }

class GammaSignature_InhibGmax_20(GammaSignature):

    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 500,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        },

        "GabaSyn": {
            'gmax': 2,
            'tau2': 100,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        }
    }

class GammaSignature_InhibGmax_30(GammaSignature):

    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 500,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        },

        "GabaSyn": {
            'gmax': 3,
            'tau2': 100,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        }
    }