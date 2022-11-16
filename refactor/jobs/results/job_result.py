from typing import Union, Dict, Any, Tuple
from drf_yasg.openapi import Schema, FORMAT_UUID, TYPE_STRING, TYPE_INTEGER
import json
import numpy as np

from jobs.results.job_status import JobStatus
from tracer.metrics.supported_trace_metric import SupportedTraceMetric


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
    IDS = "ids"
    SOURCE = "source"
    TARGET = "target"
    SCORE = "score"
    SOURCE_TARGET_PAIRS = "source_target_pairs"

    _MINIMIZE = "minimize"
    _MAXIMIZE = "minimize"
    _comparison_metric = ("_loss", _MINIMIZE)
    _properties = {JOB_ID: Schema(type=TYPE_STRING, format=FORMAT_UUID),
                   STATUS: Schema(type=TYPE_INTEGER),
                   MODEL_PATH: Schema(type=TYPE_STRING),
                   EXCEPTION: Schema(type=TYPE_STRING)}

    def __init__(self, result_dict: Dict = None):
        self.__result = result_dict if result_dict else {}

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
            raise Exception("Unknown key. Please match expected response name.")
        self.__result[key] = value

    def __contains__(self, key: str) -> bool:
        """
        Returns True if the key is in the results dictionary
        :param key: the key to the results dictionary
        :return: True if the key is in the results dictionary else False
        """
        return key in self.__result

    def set_comparison_metric(self, metric: Union[str, SupportedTraceMetric], maximize: bool = True) -> None:
        """
        Sets the metric to compare to results (note: metrics must be set inside of result)
        :param metric: the metric to use for comparison
        :param maximize: if True, the metric results are best when value is maximized, otherwise better results mean minimized val
        :return: None
        """
        if isinstance(metric, SupportedTraceMetric):
            metric = SupportedTraceMetric.name.lower()
        self._comparison_metric = (metric, JobResult._MAXIMIZE if maximize else JobResult._MINIMIZE)

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

    def to_json(self) -> str:
        """
        Returns the job output as json
        :return: the output as json
        """
        return json.dumps(self.__result, indent=4, cls=NpEncoder)

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

    def __can_compare_with_metric(self, other: "JobResult") -> bool:
        """
         Returns True if can use comparison metric to compare the two results
         :param other: other result
         :return: True if can use comparison metric to compare the two results else false
         """
        if JobResult.METRICS in self and JobResult.METRICS in other:
            compare_metric_name, max_or_min = self._comparison_metric
            if compare_metric_name in self[JobResult.METRICS] and compare_metric_name in other[JobResult.METRICS]:
                return True
            for metric_name in self[JobResult.METRICS].keys():
                if compare_metric_name in metric_name and metric_name in other[JobResult.METRICS]:
                    self.set_comparison_metric(metric_name, max_or_min == self._MAXIMIZE)
                    return True
        return False

    def __get_comparison_vals(self, other: "JobResult") -> Tuple:
        """
        Gets the values to use for comparison
        :param other: the other result
        :return: the values to use for comparison
        """
        compare_metric_name, _ = self._comparison_metric
        if self.__can_compare_with_metric(other):
            return self[JobResult.METRICS][compare_metric_name], other[JobResult.METRICS][compare_metric_name]
        return self.get_job_status(), other.get_job_status

    def is_better_than(self, other) -> bool:
        """
        Evaluates whether this result is better than the other result
        :param other: the other result
        :return: True if this result is better than the other result else False
        """
        should_maximize = self._comparison_metric[1] == self._MAXIMIZE if self.__can_compare_with_metric(other) \
            else True
        if should_maximize:
            return self >= other
        return self <= other

    def __eq__(self, other):
        self_val, other_val = self.__can_compare_with_metric(other)
        return self_val == other_val

    def __gt__(self, other):
        self_val, other_val = self.__can_compare_with_metric(other)
        return self_val > other_val
