from typing import Dict

import datasets
from sklearn.metrics import precision_recall_curve

from config.constants import K_METRIC_DEFAULT
from data.datasets.trace_matrix import TraceMatrix
from train.metrics.abstract_trace_metric import AbstractTraceMetric

_DESCRIPTION = """
The F1 score can be interpreted as a harmonic mean of the precision and recall, where an F1 
score reaches its best value at 1 and worst score at 0. The relative contribution of precision
 and recall to the F1 score are equal.
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions (`list` of `float`): Predicted labels.
    references (`list` of `int`): Ground truth labels.
Returns:
    f1_score (`float` or `int`): F1 score. 
"""

_CITATION = """
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class FMetric(AbstractTraceMetric):
    name = "f1"

    # TODO
    def _compute(self, predictions, references, trace_matrix: TraceMatrix, k=K_METRIC_DEFAULT, **kwargs) -> Dict:
        """
        computes the Mean Average Precision@K or the average precision over k for recommendations shown for different links
         and averages them over all queries in the data.
        :param predictions: predicted labels
        :param labels: ground truth labels.
        :param k: considers only the subset of recommendations from rank 1 through k
        :param kwargs: any other necessary params
        :return: Mean Average Precision@K score.
        """
        precision, recall, thresholds = precision_recall_curve(references, predictions)
        max_f1 = 0
        max_f2 = 0
        for p, r, tr in zip(precision, recall, thresholds):
            f1 = self.f1_score(p, r)
            f2 = self.f2_score(p, r)
            if f1 >= max_f1:
                max_f1 = f1
            if f2 >= max_f2:
                max_f2 = f2
        return {"f1": max_f1, "f2": max_f2}

    def f1_score(self, precision, recall):
        return 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0

    def f2_score(self, precision, recall):
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
