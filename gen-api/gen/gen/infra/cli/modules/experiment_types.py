from gen_common.util.supported_enum import SupportedEnum
from gen_common.jobs import EnsembleExperiment
from gen_common.jobs import Experiment


class ExperimentTypes(SupportedEnum):
    """
    The types of experiments that can be constructed by script.
    """
    BASE = Experiment
    ENSEMBLE = EnsembleExperiment
