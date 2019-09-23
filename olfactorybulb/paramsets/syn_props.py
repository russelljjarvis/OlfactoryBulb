from olfactorybulb.paramsets.case_studies import *

class MCsWithGJsGCsExc_0(MCsWithGJsGCs):

    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 0,

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

class MCsWithGJsGCsExc_10(MCsWithGJsGCs):

    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 10,

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

class MCsWithGJsGCsExc_100(MCsWithGJsGCs):

    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 100,

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

class MCsWithGJsGCsExc_1000(MCsWithGJsGCs):

    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 1000,

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

class MCsWithGJsGCsExc_10000(MCsWithGJsGCs):

    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 10000,

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






class TCsWithGJsGCsExc_0(TCsWithGJsGCs):
    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 0,

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

class TCsWithGJsGCsExc_10(TCsWithGJsGCs):
    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 10,

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

class TCsWithGJsGCsExc_100(TCsWithGJsGCs):
    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 100,

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

class TCsWithGJsGCsExc_1000(TCsWithGJsGCs):
    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 1000,

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

class TCsWithGJsGCsExc_10000(TCsWithGJsGCs):
    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 10000,

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
    
    
    
    
# -------- Inhibitory gmax ------------ #

class MCsWithGJsGCsInhib_0(MCsWithGJsGCs):

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

class MCsWithGJsGCsInhib_1(MCsWithGJsGCs):

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

class MCsWithGJsGCsInhib_2(MCsWithGJsGCs):

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

class MCsWithGJsGCsInhib_4(MCsWithGJsGCs):

    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 500,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        },

        "GabaSyn": {
            'gmax': 4,
            'tau2': 100,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        }
    }

class MCsWithGJsGCsInhib_8(MCsWithGJsGCs):

    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 500,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        },

        "GabaSyn": {
            'gmax': 8,
            'tau2': 100,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        }
    }






class TCsWithGJsGCsInhib_0(TCsWithGJsGCs):

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

class TCsWithGJsGCsInhib_1(TCsWithGJsGCs):

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

class TCsWithGJsGCsInhib_2(TCsWithGJsGCs):

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

class TCsWithGJsGCsInhib_4(TCsWithGJsGCs):

    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 500,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        },

        "GabaSyn": {
            'gmax': 4,
            'tau2': 100,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        }
    }

class TCsWithGJsGCsInhib_8(TCsWithGJsGCs):

    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 500,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        },

        "GabaSyn": {
            'gmax': 8,
            'tau2': 100,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        }
    }


# -------- Inhibitory tau2 ------------ #

class MCsWithGJsGCsTau2_1(MCsWithGJsGCs):
    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 500,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        },

        "GabaSyn": {
            'gmax': 2,
            'tau2': 1,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        }
    }


class MCsWithGJsGCsTau2_10(MCsWithGJsGCs):
    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 500,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        },

        "GabaSyn": {
            'gmax': 2,
            'tau2': 10,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        }
    }


class MCsWithGJsGCsTau2_100(MCsWithGJsGCs):
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


class MCsWithGJsGCsTau2_1000(MCsWithGJsGCs):
    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 500,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        },

        "GabaSyn": {
            'gmax': 2,
            'tau2': 1000,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        }
    }


class TCsWithGJsGCsTau2_1(TCsWithGJsGCs):
    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 500,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        },

        "GabaSyn": {
            'gmax': 2,
            'tau2': 1,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        }
    }


class TCsWithGJsGCsTau2_10(TCsWithGJsGCs):
    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 500,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        },

        "GabaSyn": {
            'gmax': 2,
            'tau2': 10,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        }
    }


class TCsWithGJsGCsTau2_100(TCsWithGJsGCs):
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


class TCsWithGJsGCsTau2_1000(TCsWithGJsGCs):
    synapse_properties = {
        "AmpaNmdaSyn": {
            'gmax': 500,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        },

        "GabaSyn": {
            'gmax': 2,
            'tau2': 1000,

            'ltpinvl': 0,  # Disable plasticity
            'ltdinvl': 0
        }
    }


