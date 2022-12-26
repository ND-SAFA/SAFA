from typing import List, Union, Type

from config.override import overrides
from util.variables.definition_variable import DefinitionVariable
from util.variables.experimental_variable import ExperimentalVariable
from jobs.abstract_job import AbstractJob
from jobs.supported_job_type import SupportedJobType
from train.metrics.supported_trace_metric import SupportedTraceMetric
from util.base_object import BaseObject


class ExperimentStep(BaseObject):
    def __init__(self, jobs: Union[List[AbstractJob], ExperimentalVariable],
                 comparison_metric: Union[str, SupportedTraceMetric] = None, should_maximize_metric: bool = True):
        """
        Represents an experiment step
        :param jobs: all the jobs to run in this step
        :param comparison_metric: the metric to use to determine the best job
        :param should_maximize_metric: True if should maximize the comparison metric to find best job
        """
        self.jobs = jobs.get_values_of_all_variables() if isinstance(jobs, ExperimentalVariable) else jobs
        self.comparison_metric = comparison_metric
        self.should_maximize_metric = should_maximize_metric

    def run(self, prior_best_job: AbstractJob = None) -> AbstractJob:
        """
        Runs all step jobs
        :param prior_best_job: the best job from a prior step
        :return: the best job from this step
        """
        if prior_best_job:
            if hasattr(prior_best_job, "model_manager"):
                prior_best_job.model_manager.model_path = prior_best_job.output_dir  # TODO is this right?
            self._run_on_all_jobs(self.jobs, "use_values_from_object_for_undetermined", obj=prior_best_job)
        self._run_on_all_jobs(self.jobs, "start")
        self._run_on_all_jobs(self.jobs, "join")
        return self._get_best_job(self.jobs, self.comparison_metric, self.should_maximize_metric)

    @staticmethod
    def _run_on_all_jobs(jobs: List[AbstractJob], method_name: str, **method_params) -> List:
        """
        Runs a method on all jobs in the list
        :param jobs: the list of jobs to run the method on
        :param method_name: the method to run
        :param method_params: any parameters to use in the method
        :return: list of results
        """
        return list(map(lambda job: getattr(job, method_name)(**method_params), jobs))

    @staticmethod
    def _get_best_job(jobs: List[AbstractJob], comparison_metric: Union[str, SupportedTraceMetric] = None,
                      should_maximize: bool = True) -> AbstractJob:
        """
        Returns the job with the best results as determined by the comparison info
        :param jobs: the list of all jobs
        :param comparison_metric: the metric to use to determine the best job
        :param should_maximize: True if should maximize the comparison metric to find best job
        :return: the best job
        """
        best_job = jobs[0]
        if comparison_metric:
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

    @classmethod
    @overrides(BaseObject)
    def initialize_from_definition(cls, definition: DefinitionVariable):
        """
        Initializes the obj from a dictionary
        :param definition: a dictionary of the necessary params to initialize
        :return: the initialized obj
        """
        instance = super().initialize_from_definition(definition)
        if isinstance(instance.jobs, list) and isinstance(instance.jobs[0], ExperimentalVariable):
            instance.jobs = instance.jobs.pop().get_values_of_all_variables()  # TODO why is this happening
        return instance
