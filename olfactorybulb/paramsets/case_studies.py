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
        "MC": 4,
        # "TC": 0,
    }

    mc_input_weight = 1.0

class PureTCsWithGJs(SilentNetwork):

    description = "Pure TC input and enabled gap junctions"

    gap_juction_gmax = {
        # "MC": 0,
        "TC": 4,
    }

    tc_input_weight = 1.0

class MCsWithGJsGCs(SilentNetwork):

    gap_juction_gmax = {
        "MC": 4,
    }

    mc_input_weight = 1.0

    tstop = 400

    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 64,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        },

        "GabaSyn": {
            'gmax': 0,
            'tau2': 64,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        }
    }

class TCsWithGJsGCs(SilentNetwork):

    gap_juction_gmax = {
        "TC": 32,
    }

    tc_input_weight = 1.0

    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 64,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        },

        "GabaSyn": {
            'gmax': 0,
            'tau2': 64,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        }
    }



class MC_TC_Combined_Base(TCsWithGJsGCs):

    gap_juction_gmax = {
        "MC": 32,
        "TC": 32,
    }

    mc_input_weight = 1.0
    tc_input_weight = 1.0

class GammaSignature(MC_TC_Combined_Base):

    sniffs = 3
    tstop = (1+sniffs) * 200

    tc_input_weight = 0.8
    mc_input_weight = 0.2
    mc_input_delay = 0

    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 64,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        },

        "GabaSyn": {
            'gmax': 2,
            'tau2': 16,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        }
    }