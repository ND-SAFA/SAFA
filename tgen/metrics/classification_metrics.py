from typing import Dict

import datasets
from sklearn.metrics import precision_score, recall_score

from tgen.data.tdatasets.trace_matrix import TraceMatrix
from tgen.metrics.abstract_trace_metric import AbstractTraceMetric

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
class ClassificationMetrics(AbstractTraceMetric):
    name = "precision"
    PRECISION_KEY = "precision"
    RECALL_KEY = "recall"

    def _compute(self, predictions, references, trace_matrix: TraceMatrix = None, **kwargs) -> Dict:
        """
        Computes the Precision@K or the percentage of links that were correctly predicted
        :param predictions: predicted labels
        :param references: ground truth labels.
        :param trace_matrix: Matrix used to calculate trace metrics.
        :param k: considers only the subset of recommendations from rank 1 through k
        :param kwargs: any other necessary params
        :return: Precision@K score.
        """
        predictions = list(map(lambda p: 1 if p >= 0.5 else 0, predictions))
        precision = precision_score(references, predictions)
        recall = recall_score(references, predictions)
        f1 = self.f1_score(precision, recall)
        f2 = self.f2_score(precision, recall)
        metrics = {"precision": precision, "recall": recall, "f1": f1, "f2": f2}
        return metrics

    @staticmethod
    def f1_score(precision, recall):
        """
        Returns the f1 score from precision and recall.
        :param precision: The precision score.
        :param recall: The recall score
        :return: The harmonic mean between precision and recall.
        """
        return 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0

    @staticmethod
    def f2_score(precision, recall):
        """
        Returns the F2 score from precision and recall.
        :param precision: The precision score.
        :param recall: The recall score
        :return: The harmonic mean between precision and recall with greater weight to recall.
        """
        return 5 * precision * recall / (4 * precision + recall) if precision + recall > 0 else 0

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
