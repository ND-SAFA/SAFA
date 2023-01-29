import os
from copy import deepcopy
from typing import Any, Dict, List, Optional, Type, Union

import math

from config.override import overrides
from jobs.abstract_job import AbstractJob
from jobs.abstract_trace_job import AbstractTraceJob
from jobs.components.job_result import JobResult
from jobs.supported_job_type import SupportedJobType
from jobs.train_job import TrainJob
from train.save_strategy.comparison_criteria import ComparisonCriterion
from util.base_object import BaseObject
from util.file_util import FileUtil
from util.json_util import JsonUtil
from util.status import Status
from variables.experimental_variable import ExperimentalVariable


class ExperimentStep(BaseObject):
    """
    Container for parallel jobs to run.
    """
    OUTPUT_FILENAME = "output.json"
    MAX_JOBS = 1
    RUN_ASYNC = False
    EXIT_ON_FAILED_JOB = True

    def __init__(self, jobs: Union[List[AbstractJob], ExperimentalVariable], comparison_criterion: ComparisonCriterion = None):
        """
        Initialized step with jobs and comparison criterion for determining best job.
        :param jobs: all the jobs to run in this step
        :param comparison_criterion: The criterion used to determine the best job.
        """
        if not isinstance(jobs, ExperimentalVariable):
            jobs = ExperimentalVariable(jobs)
        jobs, experimental_vars = jobs.get_values_of_all_variables(), jobs.experimental_param_names_to_vals
        self.jobs = self._update_jobs_with_experimental_vars(jobs, experimental_vars)
        self.status = Status.NOT_STARTED
        self.best_job = None
        self.comparison_criterion = comparison_criterion
        if not self.RUN_ASYNC:
            self.MAX_JOBS = 1

    def run(self, output_dir: str, jobs_for_undetermined_vars: List[AbstractJob] = None) -> List[AbstractJob]:
        """
        Runs all step jobs
        :param output_dir: the directory to save to
        :param jobs_for_undetermined_vars: the best job from a prior step
        :return: the best job from this step if comparison metric is provided, else all the jobs
        """
        self.status = Status.IN_PROGRESS
        if jobs_for_undetermined_vars:
            self.jobs = self._update_jobs_undetermined_vars(self.jobs, jobs_for_undetermined_vars)
        self.jobs = self._update_job_children_output_paths(self.jobs, output_dir)
        use_multi_epoch_step = isinstance(self.jobs[0], TrainJob) and self.jobs[0].trainer_args.train_epochs_range is not None
        job_runs = self._divide_jobs_into_runs()

        for jobs in job_runs:
            if use_multi_epoch_step:
                self.best_job = self._run_multi_epoch_step(jobs, output_dir)
            else:
                self.best_job = self._run_jobs(jobs, output_dir)
            failed_jobs = self._get_failed_jobs(jobs)
            if len(failed_jobs) > 0 and self.EXIT_ON_FAILED_JOB:
                self.status = Status.FAILURE
                break

        if self.status != Status.FAILURE:
            self.status = Status.SUCCESS
        self.save_results(output_dir)
        return [self.best_job] if self.best_job else self.jobs

    def save_results(self, output_dir: str) -> None:
        """
        Saves the results of the step
        :param output_dir: the directory to output results to
        :return: None
        """
        FileUtil.create_dir_safely(output_dir)
        json_output = JsonUtil.dict_to_json(self.get_results())
        output_filepath = os.path.join(output_dir, ExperimentStep.OUTPUT_FILENAME)
        FileUtil.save_to_file(json_output, output_filepath)

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

    def _run_multi_epoch_step(self, jobs: List[AbstractJob], output_dir: str) -> AbstractJob:
        """
        Runs the a multi epoch step for a given epoch range inside the jobs' trainer args
        :param jobs: a list of jobs to run
        :param output_dir: path to produce output to
        :return: the best job
        """
        from experiments.multi_epoch_experiment_step import MultiEpochExperimentStep
        best_job = None
        for job in jobs:
            multi_epoch_experiment_step = MultiEpochExperimentStep([job], self.comparison_metric,
                                                                   self.should_maximize_metric)
            best_epoch_job = multi_epoch_experiment_step.run(output_dir)
            best_job = self._get_best_job(best_epoch_job, self.best_job)
        return best_job

    def _run_jobs(self, jobs: List[AbstractJob], output_dir: str) -> AbstractJob:
        """
        Runs the jobs and returns the current best job from all runs
        :param jobs: a list of jobs to run
        :param output_dir: path to produce output to
        :return: the best job
        """
        self._run_on_jobs(jobs, "start")
        self._run_on_jobs(jobs, "join")
        best_job = self._get_best_job(jobs, self.best_job)
        self._run_on_jobs(jobs, "save", output_dir=output_dir)
        return best_job

    @staticmethod
    def _get_failed_jobs(jobs: List[AbstractJob]) -> List[str]:
        """
        Returns a list of a failed job ids
        :param jobs: a list of jobs to check which failed
        :return: a list of a failed job ids
        """
        return [job.id for job in jobs if job.result.get_job_status() == Status.FAILURE]

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

    def _get_best_job(self, jobs: List[AbstractJob], best_job: AbstractJob = None) -> Optional[AbstractJob]:
        """
        Returns the job with the best results as determined by the comparison info
        :param jobs: the list of all jobs
        :param best_job: the current best job
        :return: the best job
        """
        if self.comparison_criterion is None:
            return None
        best_job = best_job if best_job else jobs[0]
        for job in jobs:
            if isinstance(job, AbstractTraceJob):
                if best_job is None or job.result.is_better_than(best_job.result, self.comparison_criterion):
                    best_job = job
        return best_job

    @staticmethod
    def _update_jobs_with_experimental_vars(jobs: List[AbstractJob], experimental_vars: List[Dict[str, Any]]) -> List[AbstractJob]:
        """
        Updates the jobs to contain the experimental vars associated with that job
        :param jobs: the jobs to update
        :param experimental_vars: the list of experimental vars associated with each job
        :return: the update jobs
        """
        for i, job in enumerate(jobs):
            if not job.result[JobResult.EXPERIMENTAL_VARS]:
                job.result[JobResult.EXPERIMENTAL_VARS] = {}
            if experimental_vars:
                job.result[JobResult.EXPERIMENTAL_VARS].update(experimental_vars[i])
        return jobs

    def _update_jobs_undetermined_vars(self, jobs2update: List[AbstractJob], jobs2use: List[AbstractJob]) -> List[AbstractJob]:
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

    @staticmethod
    def _update_job_children_output_paths(jobs: List[AbstractJob], output_dir: str) -> List[AbstractJob]:
        """
        Updates necessary job children output paths to reflect experiment step output path
        :param jobs: the list of jobs to update
        :param output_dir: the output directory to use
        :return: the updated jobs
        """
        for job in jobs:
            if isinstance(job, AbstractTraceJob):
                if getattr(job.model_manager, "output_dir", "ignore") is None:
                    setattr(job.model_manager, "output_dir", output_dir)
        return jobs
