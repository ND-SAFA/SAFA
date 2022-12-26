from experiments.experiment import Experiment
from experiments.variables.definition_variable import DefinitionVariable


class ExperimentFactory:

    def __init__(self, experiment_definition: DefinitionVariable):
        """
         Responsible for creating experiments
         :param experiment_definition: all necessary parameters for creating the experiment (may be json or definition var)
         """
        if not isinstance(experiment_definition, DefinitionVariable):
            # TODO @alberto please add serializing to this
            pass
        self.experiment_definition = experiment_definition

    def build(self) -> Experiment:
        """
        Creates experiment using the experiment definition
        :return: the Experiment
        """
        return Experiment.initialize_from_definition(self.experiment_definition)

