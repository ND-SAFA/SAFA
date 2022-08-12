from datasets import list_metrics
from trace.metrics.map_at_k_metric import MapAtKMetric
from trace.metrics.mrr_metric import MRRMetric
from trace.metrics.precision_at_k_metric import PrecisionAtKMetric

SUPPORTED_METRICS = {MapAtKMetric.name: MapAtKMetric.path,
                     PrecisionAtKMetric.name: PrecisionAtKMetric.path,
                     MRRMetric.name: MRRMetric.path}


def get_metric_path(metric_name: str) -> str:
    """
    Gets the path required to load a metric
    :param metric_name: name of the metric
    :return: the path to the metric
    """
    if metric_name in SUPPORTED_METRICS:
        path = SUPPORTED_METRICS[metric_name]
    elif metric_name in list_metrics:
        path = metric_name
    else:
        raise NameError("Metric %s is unknown" % metric_name)
    return path
