from datasets import list_metrics
from results.metrics.map_at_k import MAPatK
from results.metrics.mrr import MRR
from results.metrics.precision_at_k import PrecisionAtK
from constants import PROJ_PATH
import os

SUPPORTED_METRICS = {MAPatK.name: MAPatK.path,
                     PrecisionAtK.name: PrecisionAtK.path,
                     MRR.name: MRR.path}


def get_metric_path(metric_name: str) -> str:
    if metric_name in SUPPORTED_METRICS:
        path = SUPPORTED_METRICS[metric_name]
    elif metric_name in list_metrics:
        path = metric_name
    else:
        raise NameError("Metric %s is unknown" % metric_name)
    return path
