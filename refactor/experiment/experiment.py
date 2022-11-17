import itertools
from dataclasses import dataclass, field
from typing import List, Dict, Type, Optional, Tuple, Union, Any

from config.constants import USE_BEST_FROM_PREVIOUS
from jobs.abstract_job import AbstractJob
from jobs.job_factory import JobFactory
from tracer.metrics.supported_trace_metric import SupportedTraceMetric


@dataclass
class JobVariables:
    """
    The type of job (e.g. Predict/Train)
    """
    job_type: Type[AbstractJob]
    """
    A dictionary containing name, value mappings for all constant variables
    """
    constant: Dict[str, Any] = field(default_factory=dict)
    """
    A dictionary containing name, list of possible value mappings for all experimental variables
    """
    experimental: Dict[str, List] = field(default_factory=dict)
    """
    An optional tuple containing the metric to use to determine the best job and a bool that if True will aim to maximize the metric 
    else minimize it
    """
    comparison_info: Tuple[Union[str, SupportedTraceMetric], bool] = None
    """
    Initialized post init to determine all different combinations of the experimental vars
    """
    all_experimental_combinations: List[Dict] = field(init=False)
    """
    True if any of the constant variables require the best value from a previous job
    """
    use_best_from_previous: bool = field(init=False)

    def __post_init__(self):
        self.all_experimental_combinations = self._get_all_combinations_of_experimental_vars()
        self.use_best_from_previous = self._use_best_from_previous()

    def _get_all_combinations_of_experimental_vars(self) -> List[Dict[str, Any]]:
        """
        Returns a list of all possible combinations of experimental variables
        :return: a list of all possible combinations of experimental variables
        """
        var_names = list(self.experimental.keys())
        experimental_var_combinations = list(itertools.product(*[self.experimental[name] for name in var_names]))
        return [{var_names[i]: experimental_vars[i] for i in range(len(var_names))}
                for experimental_vars in experimental_var_combinations]

    def _use_best_from_previous(self):
        """
        Determines whether the step should use best
        :param job_vars:
        :return:
        """
        for var_val in self.constant.values():
            if var_val == USE_BEST_FROM_PREVIOUS:
                return True
        return False


class ExperimentStep:
    def __init__(self, job_vars: JobVariables):
        """
        Represents an experiment step
        :param job_vars: variables to explore in this step
        """
        self.job_vars = job_vars
        self.job_factories = self._make_factories(job_vars)

    def run(self, **prior_bests) -> AbstractJob:
        """
        Runs all step jobs
        :param prior_bests: optional kwargs from previous step bests to fill in missing job params
        :return: the best job from this step
        """
        jobs = self._build_jobs(**prior_bests)
        self._start_jobs(jobs)
        self._finish_jobs(jobs)
        return self._get_best_job(jobs, self.job_vars.comparison_info) if self.job_vars.comparison_info else jobs[0]

    def _build_jobs(self, **prior_bests) -> List[AbstractJob]:
        """
        Builds the jobs from the factories
        :param prior_bests: optional kwargs from previous step bests to fill in missing job params
        :return: the list of jobs
        """
        jobs = []
        for factory in self.job_factories:
            if self.job_vars.use_best_from_previous:  # TODO: filter out any args that are not needed
                factory.set_args(**prior_bests)
            job = factory.build(self.job_vars.job_type)
            jobs.append(job)
        return jobs

    @staticmethod
    def _make_factories(job_vars: JobVariables) -> List[JobFactory]:
        """
        Creates job factories for each combination of job variable
        :param job_vars: the job variables
        :return: a list of job factories
        """
        if len(job_vars.experimental) < 1:
            return [JobFactory(**job_vars.constant)]
        return [JobFactory(**job_vars.constant, **experimental_vars) for experimental_vars in job_vars.all_experimental_combinations]

    @staticmethod
    def _start_jobs(jobs: List[AbstractJob]) -> None:
        """
        Starts all jobs
        :param jobs: list of jobs
        :return: None
        """
        map(lambda job: job.start(), jobs)

    @staticmethod
    def _finish_jobs(jobs: List[AbstractJob]) -> None:
        """
        Ensures all jobs complete
        :param jobs: list of jobs
        :return: None
        """
        map(lambda job: job.join(), jobs)

    @staticmethod
    def _get_best_job(jobs: List[AbstractJob], comparison_info: Tuple[Union[str, SupportedTraceMetric], bool]) -> AbstractJob:
        """
        Returns the job with the best results as determined by the comparison info
        :param jobs: the list of all jobs
        :param comparison_info: a tuple containing the metric to determine the best job and a bool that if True will aim to maximize
                                the metric else minimize it
        :return: the best job
        """
        comparison_metric, should_maximize = comparison_info
        best_job = jobs[0]
        for job in jobs:
            if job.result.is_better_than(best_job, comparison_metric, should_maximize):
                best_job = job
        return best_job


class Experiment:

    def __init__(self, jobs_vars: List[JobVariables]):
        """
        Represents an experiment run
        :param jobs_vars: list of all variables to explore
        """
        self.steps = self._make_steps(jobs_vars)

    @staticmethod
    def _make_steps(jobs_vars: List[JobVariables]) -> List[ExperimentStep]:
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
