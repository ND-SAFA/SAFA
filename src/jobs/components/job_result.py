import json
from typing import Any, Dict, Tuple, Union

import numpy as np
from drf_yasg.openapi import FORMAT_UUID, Schema, TYPE_INTEGER, TYPE_STRING

from jobs.components.job_status import JobStatus
from train.metrics.supported_trace_metric import SupportedTraceMetric
from util.uncased_dict import UncasedDict


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


class JobResult:
    JOB_ID = "jobID"
    EXCEPTION = "exception"
    STATUS = "status"
    MODEL_PATH = "modelPath"
    TRACEBACK = "traceback"
    PREDICTIONS = "predictions"
    ARTIFACT_IDS = "ids"
    METRICS = "metrics"
    SAVED_DATASET_PATHS = "savedDatasetPaths"
    IDS = "ids"
    SOURCE = "source"
    TARGET = "target"
    SCORE = "score"
    SOURCE_TARGET_PAIRS = "source_target_pairs"

    _properties = {JOB_ID: Schema(type=TYPE_STRING, format=FORMAT_UUID),
                   STATUS: Schema(type=TYPE_INTEGER),
                   MODEL_PATH: Schema(type=TYPE_STRING),
                   EXCEPTION: Schema(type=TYPE_STRING)}

    def __init__(self, result_dict: Dict = None):
        self.__result = UncasedDict(result_dict)

    def set_job_status(self, status: JobStatus) -> None:
        """
        Sets the status of the job in teh results
        :param status: the job status
        :return: None
        """
        self[JobResult.STATUS] = status

    def get_job_status(self) -> JobStatus:
        """
        Gets the job status from results
        :return: the job status
        """
        if JobResult.STATUS in self:
            return self[JobResult.STATUS]
        return JobStatus.UNKNOWN

    def update(self, other_result: Union["JobResult", Dict]) -> "JobResult":
        """
        Merges both results into current result (replacing current value with value from other_result for overlapping keys)
        :param other_result: the other result
        :return: None
        """
        if isinstance(other_result, JobResult):
            other_result = other_result.__result
        self.__result.update(other_result)
        return self

    def to_json(self, key: str = None) -> str:
        """
        Returns the job output as json
        :return: the output as json
        """
        obj = self.__result[key] if key else self.__result
        return json.dumps(obj, indent=4, cls=NpEncoder)

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
        :param response_keys: either a single response key or a list of response keys to get properties for
        :return a dictionary of the response keys mapped to appropriate schema
        """
        if not isinstance(response_keys, list):
            response_keys = [response_keys]
        properties = {}
        for key in response_keys:
            if key in JobResult._properties:
                properties[key] = JobResult._properties[key]
        return properties

    def is_better_than(self, other: "JobResult", comparison_metric: Union[str, SupportedTraceMetric] = None,
                       should_maximize: bool = True) -> bool:
        """
        Evaluates whether this result is better than the other result
        :param other: the other result
        :param comparison_metric: metric to use for comparison (defaults to status)
        :param should_maximize: if True, a better result means maximizing the provided metric, else aims to minimize it
        :return: True if this result is better than the other result else False
        """
        if isinstance(comparison_metric, SupportedTraceMetric):
            comparison_metric = comparison_metric.name
        self_val, other_val = self._get_comparison_vals(other, comparison_metric)
        if should_maximize:
            return self_val >= other_val
        return self_val <= other_val

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

    def __repr__(self) -> dict:
        """
        Returns the results dictionary as a representation of the class
        :return: the results dict
        """
        return self.__result
