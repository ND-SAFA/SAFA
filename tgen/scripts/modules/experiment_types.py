from experiments.ensemble_experiment import EnsembleExperiment
from experiments.experiment import Experiment
from util.supported_enum import SupportedEnum


class ExperimentTypes(SupportedEnum):
    """
    The types of experiments that can be constructed by script.
    """
    BASE = Experiment
    ENSEMBLE = EnsembleExperiment
