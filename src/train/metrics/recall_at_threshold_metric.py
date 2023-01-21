from typing import Dict

import datasets
from sklearn.metrics import recall_score

from train.metrics.abstract_trace_metric import AbstractTraceMetric
from train.metrics.metrics_manager import MetricsManager

_DESCRIPTION = """
Recall@K metric measures the percentage of true links that were correctly predicted.
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions (`list` of `int`): Predicted labels.
    references (`list` of `int`): Ground truth labels.
    k (int): The level of the threshold to consider a similar score a true label.
Returns:
    recall_at_k (`float` or `int`): Recall@K score. 
"""

_CITATION = """
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class RecallAtThresholdMetric(AbstractTraceMetric):
    name = "recall@k"

    def _compute(self, predictions, references, trace_matrix: MetricsManager = None, **kwargs) -> Dict:
        """
        Recall@K metric measures the percentage of true links that were correctly predicted.
        :param predictions: predicted labels
        :param labels: ground truth labels.
        :param k: considers only the subset of recommendations from rank 1 through k
        :param kwargs: any other necessary params
        :return: Recall@K score.
        """
        score = trace_matrix.calculate_query_metric_at_k(recall_score, k)
        metric_name = self.name.replace("k", k)
        return {metric_name: score}

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
