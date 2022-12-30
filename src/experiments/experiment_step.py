import math
import os
from copy import deepcopy
from typing import Any, Callable, Dict, List, Type, Union

from config.override import overrides
from jobs.abstract_job import AbstractJob
from jobs.components.job_result import JobResult
from jobs.supported_job_type import SupportedJobType
from server.storage.safa_storage import SafaStorage
from train.metrics.supported_trace_metric import SupportedTraceMetric
from util.base_object import BaseObject
from util.file_util import FileUtil
from util.json_util import JSONUtil
from util.status import Status
from variables.experimental_variable import ExperimentalVariable


class ExperimentStep(BaseObject):
    OUTPUT_FILENAME = "output.json"
    MAX_JOBS = 1
    RUN_ASYNC = False

    def __init__(self, jobs: Union[List[AbstractJob], ExperimentalVariable, List[ExperimentalVariable]],
                 comparison_metric: Union[str, SupportedTraceMetric] = None, should_maximize_metric: bool = True):
        """
        Represents an experiment step
        :param jobs: all the jobs to run in this step
        :param comparison_metric: the metric to use to determine the best job
        :param should_maximize_metric: True if should maximize the comparison metric to find best job
        """
        if isinstance(jobs, list) and isinstance(jobs[0], ExperimentalVariable):
            jobs = jobs.pop()  # TODO fix this
        if not isinstance(jobs, ExperimentalVariable):
            jobs = ExperimentalVariable(jobs)
        jobs, experimental_vars = jobs.get_values_of_all_variables(), jobs.experimental_param_names_to_vals
        self.jobs = self._update_jobs_with_experimental_vars(jobs, experimental_vars) if experimental_vars else jobs
        self.status = Status.NOT_STARTED
        self.best_job = None
        self.comparison_metric = comparison_metric
        self.should_maximize_metric = should_maximize_metric

    def run(self, jobs_for_undetermined_vars: List[AbstractJob] = None, job_callback: Callable[[], None] = None) -> \
            List[
                AbstractJob]:
        """
        Runs all step jobs
        :param job_callback:
        :type job_callback:
        :param jobs_for_undetermined_vars: the best job from a prior step
        :return: the best job from this step if comparison metric is provided, else all the jobs
        """
        self.status = Status.IN_PROGRESS
        if jobs_for_undetermined_vars:
            self.jobs = self._update_jobs_undetermined_vars(self.jobs, jobs_for_undetermined_vars)

        if self.RUN_ASYNC:
            job_runs = self._divide_jobs_into_runs()
            for jobs in job_runs:
                self._run_on_jobs(jobs, "start")
                self._run_on_jobs(jobs, "join")
        else:
            for job in self.jobs:
                job.run()
                if job_callback:
                    job_callback()

        self.status = Status.SUCCESS
        if self.comparison_metric:
            self.best_job = self._get_best_job(self.jobs, self.comparison_metric, self.should_maximize_metric)
            return [self.best_job]
        return self.jobs

    def save_results(self, output_dir: str) -> None:
        """
        Saves the results of the step
        :param output_dir: the directory to output results to
        :return: None
        """
        FileUtil.make_dir_safe(output_dir)
        json_output = JSONUtil.dict_to_json(self.get_results())
        output_filepath = os.path.join(output_dir, ExperimentStep.OUTPUT_FILENAME)
        SafaStorage.save_to_file(json_output, output_filepath)
        for job in self.jobs:
            job.save(output_dir)

    def get_results(self) -> Dict[str, str]:
        """
        Gets the results of the step
        :return: a dictionary containing the results
        """
        results = {}
        for var_name, var_value in vars(self).items():
            if var_name.startswith("_") or callable(var_value):
                continue
            results[var_name] = var_value
        return results

    def _divide_jobs_into_runs(self) -> List[List[AbstractJob]]:
        """
        Divides the jobs up into runs of size MAX JOBS
        :return: a list of runs containing at most MAX JOBS per run
        """
        job_runs = [[] for i in range(math.ceil(len(self.jobs) / self.MAX_JOBS))]
        run_index = 0
        for job_index, job in enumerate(self.jobs):
            job_runs[run_index].append(job)
            if (job_index + 1) % self.MAX_JOBS == 0:
                run_index += 1
        return job_runs

    @staticmethod
    def _update_jobs_with_experimental_vars(jobs: List[AbstractJob], experimental_vars: List[Dict[str, Any]]) -> List[
        AbstractJob]:
        """
        Updates the jobs to contain the experimental vars associated with that job
        :param jobs: the jobs to update
        :param experimental_vars: the list of experimental vars associated with each job
        :return: the update jobs
        """
        for i, job in enumerate(jobs):
            job.result[JobResult.EXPERIMENTAL_VARS] = experimental_vars[i]
        return jobs

    def _update_jobs_undetermined_vars(self, jobs2update: List[AbstractJob], jobs2use: List[AbstractJob]) -> List[
        AbstractJob]:
        """
        Updates all the jobs2update's undetermined vals with those from the jobs2use
        :param jobs2update: the list of jobs to update undetermined vals for
        :param jobs2use: the list of jobs to use for updating undetermined vals
        :return: the list of updated jobs
        """
        final_jobs = []
        for job in jobs2use:
            jobs2update_tmp = deepcopy(jobs2update)
            jobs2update = jobs2update_tmp
            if hasattr(job, "model_manager"):
                job.model_manager.model_path = job.model_manager.model_output_path
            self._run_on_jobs(jobs2update, "use_values_from_object_for_undetermined", obj=job)
            final_jobs.extend(jobs2update)
        return final_jobs

    @staticmethod
    def _run_on_jobs(jobs: List[AbstractJob], method_name: str, **method_params) -> List:
        """
        Runs a method on all jobs in the list
        :param jobs: the list of jobs to run the method on
        :param method_name: the method to run
        :param method_params: any parameters to use in the method
        :return: list of results
        """
        return list(map(lambda job: getattr(job, method_name)(**method_params), jobs))

    @staticmethod
    def _get_best_job(jobs: List[AbstractJob], comparison_metric: Union[str, SupportedTraceMetric],
                      should_maximize: bool = True) -> AbstractJob:
        """
        Returns the job with the best results as determined by the comparison info
        :param jobs: the list of all jobs
        :param comparison_metric: the metric to use to determine the best job
        :param should_maximize: True if should maximize the comparison metric to find best job
        :return: the best job
        """
        best_job = jobs[0]
        for job in jobs:
            if job.result.is_better_than(best_job.result, comparison_metric, should_maximize):
                best_job = job
        return best_job

    @classmethod
    @overrides(BaseObject)
    def _get_child_enum_class(cls, abstract_class: Type, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
        :param abstract_class: the abstract parent class type
        :param child_class_name: the name of the child class
        :return: the enum class mapping name to class
        """
        return SupportedJobType
