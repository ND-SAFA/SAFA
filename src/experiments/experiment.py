from typing import List

from experiments.experiment_step import ExperimentStep
from experiments.experiment_variables import ExperimentVariables


class Experiment:

    def __init__(self, jobs_vars: List[ExperimentVariables]):
        """
        Represents an experiment run
        :param jobs_vars: list of all variables to explore
        """
        self.steps = self._make_steps(jobs_vars)

    @staticmethod
    def _make_steps(jobs_vars: List[ExperimentVariables]) -> List[ExperimentStep]:
        """
        Constructs the experiment steps for each set of job variables
        :param jobs_vars: a list of job variables
        :return: a list of experiment steps
        """
        return [ExperimentStep(job_vars) for job_vars in jobs_vars]

    def run(self):
        """
        Runs all steps in the experiment
        :return: None
        """
        best_job_args_from_prior = {}
        for step in self.steps:
            best_job = step.run(**best_job_args_from_prior)
            best_job_args_from_prior = best_job.job_args.as_kwargs()
