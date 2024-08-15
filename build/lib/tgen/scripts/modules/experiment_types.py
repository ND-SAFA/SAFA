from common_resources.tools.util.supported_enum import SupportedEnum
from tgen.experiments.ensemble_experiment import EnsembleExperiment
from tgen.experiments.experiment import Experiment


class ExperimentTypes(SupportedEnum):
    """
    The types of experiments that can be constructed by script.
    """
    BASE = Experiment
    ENSEMBLE = EnsembleExperiment
