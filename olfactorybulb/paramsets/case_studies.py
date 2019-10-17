from olfactorybulb.paramsets.base import SilentNetwork

class PureMCs(SilentNetwork):

    description = "Pure MC input"
    mc_input_weight = 1.0

class PureTCs(SilentNetwork):

    description = "Pure TC input"
    tc_input_weight = 1.0

class PureMCsWithGJs(SilentNetwork):

    description = "Pure MC input and enabled gap junctions"

    gap_juction_gmax = {
        "MC": 16,
        # "TC": 0,
    }

    mc_input_weight = 1.0

class PureTCsWithGJs(SilentNetwork):

    description = "Pure TC input and enabled gap junctions"

    gap_juction_gmax = {
        # "MC": 0,
        "TC": 16,
    }

    tc_input_weight = 1.0

class MCsWithGJsGCs(SilentNetwork):

    gap_juction_gmax = {
        "MC": 16,
    }

    mc_input_weight = 1.0

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

class TCsWithGJsGCs(SilentNetwork):

    gap_juction_gmax = {
        "TC": 16,
    }

    tc_input_weight = 1.0

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



class MC_TC_Combined_Base(SilentNetwork):

    gap_juction_gmax = {
        "MC": 16,
        "TC": 16,
    }

    mc_input_weight = 1.0
    tc_input_weight = 1.0

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

class GammaSignature(MC_TC_Combined_Base):

    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.75
    mc_input_delay = 20