import inspect
from typing import List, Set, Type

from datasets import Metric, list_metrics

from common_resources.tools.util.supported_enum import SupportedEnum
from common_resources.traceability.metrics.abstract_trace_metric import AbstractTraceMetric
from common_resources.traceability.metrics.average_true_links_metrics import AverageTrueLinksMetric
from common_resources.traceability.metrics.classification_metrics import ClassificationMetrics
from common_resources.traceability.metrics.confusion_matrix_at_threshold_metric import ConfusionMatrixAtThresholdMetric
from common_resources.traceability.metrics.lag_metric import LagMetric
from common_resources.traceability.metrics.map_at_k_metric import MapAtKMetric
from common_resources.traceability.metrics.map_metric import MapMetric
from common_resources.traceability.metrics.pos_link_indices import PositiveLinkIndices
from common_resources.traceability.metrics.precision_at_recall_metric import PrecisionAtRecallMetric
from common_resources.traceability.metrics.precision_at_threshold_metric import PrecisionAtKMetric
from common_resources.traceability.metrics.specificity_metric import SpecificityMetric

metric_suffix = "Metric"


class SupportedTraceMetric(SupportedEnum):
    """
    Enumerates trace metrics.
    """
    MAP = MapMetric
    PRECISION_AT_RECALL = PrecisionAtRecallMetric
    CONFUSION_MATRIX = ConfusionMatrixAtThresholdMetric
    LAG = LagMetric
    CLASSIFICATION = ClassificationMetrics
    PRECISION_AT_K = PrecisionAtKMetric
    AVERAGE_TRUE_LINKS = AverageTrueLinksMetric
    SPECIFICITY = SpecificityMetric

    @staticmethod
    def get_score_based_metrics() -> Set[str]:
        """
        :return: Returns the metrics that rely on scores.
        """
        metrics = {SupportedTraceMetric.LAG, SupportedTraceMetric.MAP, SupportedTraceMetric.PRECISION_AT_K}
        return {metric.name for metric in metrics}

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
            raise NameError(f"Metric %s is unknown: `{metric_name}`")
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
