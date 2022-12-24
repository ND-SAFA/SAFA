from typing import List

from experiments.experiment_step import ExperimentStep
from util.base_object import BaseObject


class Experiment(BaseObject):

    def __init__(self, steps: List[ExperimentStep]):
        """
        Represents an experiment run
        :param steps: list of all experiment steps to run
        """
        self.steps = steps

    def run(self):
        """
        Runs all steps in the experiment
        :return: None
        """
        best_job_from_prior_step = None
        for step in self.steps:
            best_job_from_prior_step = step.run(best_job_from_prior_step)
