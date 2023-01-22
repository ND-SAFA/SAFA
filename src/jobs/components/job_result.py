from typing import Any, Dict, List, Tuple, Union

from drf_yasg.openapi import FORMAT_UUID, Schema, TYPE_INTEGER, TYPE_STRING

from train.save_strategy.comparison_criteria import ComparisonCriterion
from train.trace_output.abstract_trace_output import AbstractTraceOutput
from util.base_object import BaseObject
from util.json_util import JsonUtil
from util.status import Status
from util.uncased_dict import UncasedDict


class JobResult(BaseObject):
    JOB_ID = "jobID"
    EXCEPTION = "exception"
    STATUS = "status"
    MODEL_PATH = "modelPath"
    TRACEBACK = "traceback"
    PREDICTIONS = "predictions"
    ARTIFACT_IDS = "ids"
    METRICS = "metrics"
    TOTAL_EPOCHS = "total_epochs"  # distinguishes from epochs which does not describe global training loop
    SAVED_DATASET_PATHS = "savedDatasetPaths"
    IDS = "ids"
    SOURCE = "source"
    TARGET = "target"
    SCORE = "score"
    SOURCE_TARGET_PAIRS = "source_target_pairs"
    VAL_METRICS = "val_metrics"
    EXPERIMENTAL_VARS = "experimental_vars"

    _properties = {JOB_ID: Schema(type=TYPE_STRING, format=FORMAT_UUID),
                   STATUS: Schema(type=TYPE_INTEGER),
                   MODEL_PATH: Schema(type=TYPE_STRING),
                   EXCEPTION: Schema(type=TYPE_STRING)}

    def __init__(self, result_dict: Dict = None):
        """
        Represents the results of a job
        :param result_dict:
        """
        self.__result = UncasedDict(result_dict)

    def set_job_status(self, status: Status) -> None:
        """
        Sets the status of the job in teh results
        :param status: the job status
        :return: None
        """
        self[JobResult.STATUS] = status

    def get_job_status(self) -> Status:
        """
        Gets the job status from results
        :return: the job status
        """
        if JobResult.STATUS in self:
            return self[JobResult.STATUS]
        return Status.UNKNOWN

    def update(self, other_result: Union["JobResult", Dict]) -> "JobResult":
        """
        Merges both results into current result (replacing current value with value from other_result for overlapping data_keys)
        :param other_result: the other result
        :return: None
        """
        if isinstance(other_result, JobResult):
            other_result = other_result.__result
        self.__result.update(UncasedDict(other_result))
        return self

    def add_trace_output(self, trace_output: AbstractTraceOutput) -> None:
        """
        Adds the trace output to the job result.
        :param trace_output: The trace output to add to job result.
        :return: None
        """
        trace_output_dict = trace_output.output_to_dict()
        self.update(trace_output_dict)

    def to_json(self, keys: List[str] = None) -> str:
        """
        Returns the job output as json
        :return: the output as json
        """
        obj = {key: self.__result[key] for key in keys if key in self.__result} if keys else self.__result
        return JsonUtil.dict_to_json(obj)

    def as_dict(self) -> dict:
        """
        Returns the results as a dictionary
        :return: the results as a dictionary
        """
        return self.__result

    @staticmethod
    def from_dict(results_dict: Dict) -> "JobResult":
        """
        Creates a JobResult from a dictionary
        :return: a new JobResult
        """
        job_result = JobResult()
        return job_result.update(results_dict)

    @staticmethod
    def get_properties(response_keys: Union[str, list]) -> Dict:
        """
        Gets properties used to generate response documentation
        :param response_keys: either a single response key or a list of response data_keys to get properties for
        :return a dictionary of the response data_keys mapped to appropriate schema
        """
        if not isinstance(response_keys, list):
            response_keys = [response_keys]
        properties = {}
        for key in response_keys:
            if key in JobResult._properties:
                properties[key] = JobResult._properties[key]
        return properties

    def is_better_than(self, other: "JobResult", comparison_criterion: ComparisonCriterion = None) -> bool:
        """
        Evaluates whether this result is better than the other result
        :param other: the other result
        :param comparison_criterion: The criterion used to determine best job.
        :return: True if this result is better than the other result else False
        """
        if comparison_criterion is None:
            comparison_criterion = ComparisonCriterion(metrics=[])
        assert len(comparison_criterion.metrics) <= 1, "Expected no more than 1 metric in comparison criterion."
        comparison_metric = comparison_criterion.metrics[0] if len(comparison_criterion.metrics) > 0 else None
        self_val, other_val = self._get_comparison_vals(other, comparison_metric)
        return comparison_criterion.comparison_function.value(self_val, other_val)

    def _can_compare_with_metric(self, other: "JobResult", comparison_metric_name: str) -> bool:
        """
         Returns True if can use comparison metric to compare the two results
         :param other: other result
         :return: True if can use comparison metric to compare the two results else false
         """
        if not comparison_metric_name:
            return False
        if JobResult.METRICS in self and JobResult.METRICS in other:
            if comparison_metric_name in self[JobResult.METRICS] and comparison_metric_name in other[JobResult.METRICS]:
                return True
        return False

    def _get_comparison_vals(self, other: "JobResult", comparison_metric_name: str) -> Tuple:
        """
        Gets the values to use for comparison
        :param other: the other result
        :return: the values to use for comparison
        """
        if self._can_compare_with_metric(other, comparison_metric_name):
            return self[JobResult.METRICS][comparison_metric_name], other[JobResult.METRICS][comparison_metric_name]
        return self.get_job_status(), other.get_job_status()

    def require_properties(self, properties: List[str]) -> None:
        """
        Requires that given properties exist in result.
        :param properties: List of required properties.
        :return: None
        """
        JsonUtil.require_properties(self.__result, properties)

    def __getitem__(self, key: str) -> Any:
        """
        Returns value matching the given key in the results dictionary
        :param key: the key to the results dictionary
        :return: the value from the results dictionary
        """
        return self.__result[key]

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Sets the key to be mapped to the given value in the results dictionary
        :param key: the key to the results dictionary
        :param value: the value to be mapped to the key in the results dictionary
        :return: None
        """
        if not hasattr(self, key.upper()):
            raise ValueError("Unknown key. Please match expected response name.")

        self.__result[key] = value

    def __contains__(self, key: str) -> bool:
        """
        Returns True if the key is in the results dictionary
        :param key: the key to the results dictionary
        :return: True if the key is in the results dictionary else False
        """
        return key in self.__result

    def __eq__(self, other: "JobResult") -> bool:
        """
        Returns True if the result dictionaries for both job results are the same
        :param other: a different job result
        :return: True if the result dictionaries for both job results are the same else False
        """
        return self.__result == other.__result

    def __repr__(self) -> str:
        """
        Returns a representation of the class as a string
        :return: the results dict as a string
        """
        return repr(self.__result)
