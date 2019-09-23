from olfactorybulb.paramsets.case_studies import *

# MC weight at delay=50
class MC_TC_Combined_MC_weight_0(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0

class MC_TC_Combined_MC_weight_001(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.01

class MC_TC_Combined_MC_weight_010(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.1

class MC_TC_Combined_MC_weight_020(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.2

class MC_TC_Combined_MC_weight_050(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.5

class MC_TC_Combined_MC_weight_080(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.8

class MC_TC_Combined_MC_weight_100(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 1


# -------- MC delay at weight 1--------- #
class MC_TC_Combined_MC_delay_0(MC_TC_Combined_Base):
    mc_input_delay = 0


class MC_TC_Combined_MC_delay_10(MC_TC_Combined_Base):
    mc_input_delay = 10


class MC_TC_Combined_MC_delay_20(MC_TC_Combined_Base):
    mc_input_delay = 20


class MC_TC_Combined_MC_delay_30(MC_TC_Combined_Base):
    mc_input_delay = 30


class MC_TC_Combined_MC_delay_40(MC_TC_Combined_Base):
    mc_input_delay = 40


class MC_TC_Combined_MC_delay_50(MC_TC_Combined_Base):
    mc_input_delay = 50


class MC_TC_Combined_MC_delay_70(MC_TC_Combined_Base):
    mc_input_delay = 70



# ------- MC Weight at Delay = 20 ------------ #
class MC_TC_Combined_MC_weight_0_delay_20(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0
    mc_input_delay = 20

class MC_TC_Combined_MC_weight_001_delay_20(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.01
    mc_input_delay = 20

class MC_TC_Combined_MC_weight_010_delay_20(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.1
    mc_input_delay = 20

class MC_TC_Combined_MC_weight_020_delay_20(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.2
    mc_input_delay = 20

class MC_TC_Combined_MC_weight_050_delay_20(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.5
    mc_input_delay = 20

    input_odors = {
        0: {"name": "Apple", "rel_conc": 0.1},
        200: {"name": "Apple", "rel_conc": 0.2},
        400: {"name": "Apple", "rel_conc": 0.2},
        600: {"name": "Apple", "rel_conc": 0.2},
        800: {"name": "Apple", "rel_conc": 0.2},
        1000: {"name": "Apple", "rel_conc": 0.2}
    }

    tstop = 1200


class MC_TC_Combined_MC_weight_080_delay_20(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.8
    mc_input_delay = 20

class MC_TC_Combined_MC_weight_100_delay_20(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 1
    mc_input_delay = 20

# ------- MC Weight at Delay = 30 ------------ #
class MC_TC_Combined_MC_weight_0_delay_30(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0
    mc_input_delay = 30

class MC_TC_Combined_MC_weight_001_delay_30(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.01
    mc_input_delay = 30

class MC_TC_Combined_MC_weight_010_delay_30(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.1
    mc_input_delay = 30

    input_odors = {
        0: {"name": "Apple", "rel_conc": 0.1},
        200: {"name": "Apple", "rel_conc": 0.2},
        400: {"name": "Apple", "rel_conc": 0.2},
        600: {"name": "Apple", "rel_conc": 0.2},
        800: {"name": "Apple", "rel_conc": 0.2},
        1000: {"name": "Apple", "rel_conc": 0.2}
    }

    tstop = 1200

class MC_TC_Combined_MC_weight_020_delay_30(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.2
    mc_input_delay = 30

class MC_TC_Combined_MC_weight_050_delay_30(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.5
    mc_input_delay = 30

class MC_TC_Combined_MC_weight_080_delay_30(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.8
    mc_input_delay = 30

class MC_TC_Combined_MC_weight_100_delay_30(MC_TC_Combined_Base):
    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 1
    mc_input_delay = 30


# Effect of Gaba gmax on TCMC clusters #
class TwoGammaClusters_InhibGmax_00(TwoGammaClusters):

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

class TwoGammaClusters_InhibGmax_05(TwoGammaClusters):

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

class TwoGammaClusters_InhibGmax_10(TwoGammaClusters):

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

class TwoGammaClusters_InhibGmax_15(TwoGammaClusters):

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

class TwoGammaClusters_InhibGmax_20(TwoGammaClusters):

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

class TwoGammaClusters_InhibGmax_30(TwoGammaClusters):

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