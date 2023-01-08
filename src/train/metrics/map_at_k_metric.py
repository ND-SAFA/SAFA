from typing import Dict

import datasets
from sklearn.metrics import average_precision_score

from config.constants import K_METRIC_DEFAULT
from data.datasets.trace_matrix import TraceMatrixManager
from train.metrics.abstract_trace_metric import AbstractTraceMetric

_DESCRIPTION = """
Mean Average Precision@K metric measures the average precision over k for recommendations shown for 
different links and averages them over all queries in the data.
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions (`list` of `float`): Predicted labels.
    references (`list` of `int`): Ground truth labels.
    k (int): considers only the subset of recommendations from rank 1 through k
Returns:
    map_at_k (`float` or `int`): Mean Average Precision@K score. 
"""

_CITATION = """
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class MapAtKMetric(AbstractTraceMetric):
    name = "map@k"

    # TODO
    def _compute(self, predictions, references, trace_matrix: TraceMatrixManager, **kwargs) -> Dict:
        """
        computes the Mean Average Precision@K or the average precision over k for recommendations shown for different links
         and averages them over all queries in the data.
        :param predictions: predicted labels
        :param labels: ground truth labels.
        :param k: considers only the subset of recommendations from rank 1 through k
        :param kwargs: any other necessary params
        :return: Mean Average Precision@K score.
        """
        results = {}

        def calculate_ap(labels, preds):
            return average_precision_score(labels, preds)

        for k in K_METRIC_DEFAULT:
            score = trace_matrix.calculate_query_metric_at_k(calculate_ap, k)
            metric_name = self.name.replace("k", str(k))
            results[metric_name] = score

        return results

    def _info(self) -> datasets.MetricInfo:
        """
        Information relating to the metric
        :return: the MetricInfo object containing metric information
        """
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=self.get_features(),
            reference_urls=[""],
        )
