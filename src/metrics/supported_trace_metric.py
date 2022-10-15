import inspect
from enum import Enum
from typing import Type

from datasets import list_metrics

from metrics.abstract_trace_metric import AbstractTraceMetric
from metrics.map_at_k_metric import MapAtKMetric
from metrics.mrr_metric import MRRMetric
from metrics.precision_at_k_metric import PrecisionAtKMetric


class SupportedTraceMetric(Enum):
    MAP_AT_K = MapAtKMetric
    PRECISION_AT_K = PrecisionAtKMetric
    MRR = MRRMetric


def get_metric_path(metric_name: str) -> str:
    """
    Gets the path required to load a metric
    :param metric_name: name of the metric
    :return: the path to the metric
    """
    try:
        trace_metric_class = SupportedTraceMetric[metric_name.upper()].value
        path = _get_metric_path_from_class(trace_metric_class)
    except KeyError:
        if metric_name in list_metrics():
            path = metric_name
        else:
            raise NameError("Metric %s is unknown" % metric_name)
    return path


def _get_metric_path_from_class(trace_metric_class: Type[AbstractTraceMetric]) -> str:
    """
    Gets the path to the given metric class
    :param trace_metric_class: the metric class to get the path of
    :return: the path to the metric
    """
    return inspect.getfile(trace_metric_class)
