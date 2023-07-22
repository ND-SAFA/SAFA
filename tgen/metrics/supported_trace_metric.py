import inspect
from typing import List, Type

from datasets import Metric, list_metrics

from tgen.metrics.abstract_trace_metric import AbstractTraceMetric
from tgen.metrics.average_true_links_metrics import AverageTrueLinksMetric
from tgen.metrics.confusion_matrix_at_threshold_metric import ConfusionMatrixAtThresholdMetric
from tgen.metrics.f1_metric import FMetric
from tgen.metrics.lag_metric import LagMetric
from tgen.metrics.map_at_k_metric import MapAtKMetric
from tgen.metrics.map_metric import MapMetric
from tgen.metrics.pos_link_indices import PositiveLinkIndices
from tgen.metrics.precision_at_recall_metric import PrecisionAtRecallMetric
from tgen.metrics.precision_at_threshold_metric import PrecisionAtKMetric
from tgen.metrics.precision_metric import ClassificationMetrics
from tgen.metrics.specificity_metric import SpecificityMetric
from tgen.util.supported_enum import SupportedEnum

metric_suffix = "Metric"


class SupportedTraceMetric(SupportedEnum):
    """
    Enumerates trace metrics.
    """
    LAG = LagMetric
    MAP = MapMetric
    CLASSIFICATION = ClassificationMetrics
    PRECISION_AT_K = PrecisionAtKMetric
    POS_INDICES = PositiveLinkIndices
    PRECISION_AT_RECALL = PrecisionAtRecallMetric
    CONFUSION_MATRIX = ConfusionMatrixAtThresholdMetric
    AVERAGE_TRUE_LINKS = AverageTrueLinksMetric
    SPECIFICITY = SpecificityMetric
    F = FMetric

    @staticmethod
    def get_query_metrics() -> List[str]:
        """
        :return: Returns the metrics that are applied on a per query basis.
        """
        return [MapMetric.name, MapAtKMetric.name, PrecisionAtKMetric.name,
                PrecisionAtRecallMetric.name, LagMetric.name, AverageTrueLinksMetric.name, PositiveLinkIndices.name]


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
