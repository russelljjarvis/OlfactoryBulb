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
        "MC": 10,
        # "TC": 0,
    }

    mc_input_weight = 1.0

class PureTCsWithGJs(SilentNetwork):

    description = "Pure TC input and enabled gap junctions"

    gap_juction_gmax = {
        # "MC": 0,
        "TC": 10,
    }

    tc_input_weight = 1.0

class MCsWithGJsGCs(SilentNetwork):

    gap_juction_gmax = {
        "MC": 8,
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
        "TC": 8,
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
        "MC": 8,
        "TC": 8,
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
            'gmax': 3,
            'tau2': 100,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        }
    }

class TwoGammaClusters(MC_TC_Combined_Base):

    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.5
    mc_input_delay = 20



class TwoGammaClusters_ExtraSniffs(MC_TC_Combined_Base):

    tc_input_weight = 1.0
    mc_input_weight = tc_input_weight * 0.1
    mc_input_delay = 35

    input_odors = {
        0: {"name": "Apple", "rel_conc": 0.1},
        200: {"name": "Apple", "rel_conc": 0.2},
        400: {"name": "Apple", "rel_conc": 0.2},
        600: {"name": "Apple", "rel_conc": 0.2},
        800: {"name": "Apple", "rel_conc": 0.2},
        1000: {"name": "Apple", "rel_conc": 0.2},
    }

    tstop = 1200