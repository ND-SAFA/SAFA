from datasets import list_metrics
from train.metrics.map_at_k import MAPatK
from train.metrics.mrr import MRR
from train.metrics.precision_at_k import PrecisionAtK

SUPPORTED_METRICS = {MAPatK.name: MAPatK.path,
                     PrecisionAtK.name: PrecisionAtK.path,
                     MRR.name: MRR.path}


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
