import inspect
from enum import Enum
from typing import Type

from datasets import Metric, list_metrics

from tracer.train.metrics.abstract_trace_metric import AbstractTraceMetric
from tracer.train.metrics.map_at_k_metric import MapAtKMetric
from tracer.train.metrics.mrr_metric import MRRMetric
from tracer.train.metrics.precision_at_k_metric import PrecisionAtKMetric

metric_suffix = "Metric"


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
        if metric_name.lower() in list_metrics():
            path = metric_name
        else:
            raise NameError("Metric %s is unknown" % metric_name)
    return path


def get_metric_name(metric_class: Metric) -> str:
    """
    Gets the metric name from its class
    :param metric_class: the class of the metric
    :return: the name
    """
    name = metric_class.name
    return name.split(metric_suffix)[0].lower()


def _get_metric_path_from_class(trace_metric_class: Type[AbstractTraceMetric]) -> str:
    """
    Gets the path to the given metric class
    :param trace_metric_class: the metric class to get the path of
    :return: the path to the metric
    """
    return inspect.getfile(trace_metric_class)
