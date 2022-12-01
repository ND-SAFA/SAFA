from typing import List, Tuple, Union

from experiments.experiment_variables import ExperimentVariables
from jobs.abstract_job import AbstractJob
from jobs.job_factory import JobFactory
from train.metrics.supported_trace_metric import SupportedTraceMetric


class ExperimentStep:
    def __init__(self, job_vars: ExperimentVariables):
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
            self._set_best_from_previous(factory, self.job_vars.best_from_previous, **prior_bests)
            job = factory.build(self.job_vars.job_type)
            jobs.append(job)
        return jobs

    @staticmethod
    def _set_best_from_previous(factory: JobFactory, best_from_previous_vars, **prior_bests):
        # TODO
        pass

    @staticmethod
    def _make_factories(job_vars: ExperimentVariables) -> List[JobFactory]:
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
