from typing import Dict

import datasets
from sklearn.metrics import precision_score

from config.constants import K_METRIC_DEFAULT
from data.datasets.trace_matrix import TraceMatrixManager
from train.metrics.abstract_trace_metric import AbstractTraceMetric

_DESCRIPTION = """
Precision@K metric measures the percentage of predicted links that were correct.
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions (`list` of `int`): Predicted labels.
    references (`list` of `int`): Ground truth labels.
    k (int): The level of the threshold to consider a similar score a true label.
Returns:
    precision_at_k (`float` or `int`): Precision@K score. 
"""

_CITATION = """
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class PrecisionAtKMetric(AbstractTraceMetric):
    name = "precision@k"

    def _compute(self, predictions, references, trace_matrix: TraceMatrixManager = None, **kwargs) -> Dict:
        """
        Computes the Precision@K or the percentage of links that were correctly predicted
        :param predictions: predicted labels
        :param labels: ground truth labels.
        :param k: considers only the subset of recommendations from rank 1 through k
        :param kwargs: any other necessary params
        :return: Precision@K score.
        """
        results = {}

        def precision(labels, preds):
            return precision_score(labels, [1] * len(preds))

        for k in K_METRIC_DEFAULT:
            score = trace_matrix.calculate_query_metric_at_k(precision, k)
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
