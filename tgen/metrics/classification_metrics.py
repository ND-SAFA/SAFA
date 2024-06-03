from typing import Dict

import datasets
from sklearn.metrics import fbeta_score, precision_score, recall_score

from tgen.common.constants.metric_constants import THRESHOLD_DEFAULT
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
        predictions = list(map(lambda p: 1 if p >= THRESHOLD_DEFAULT else 0, predictions))
        precision = precision_score(references, predictions)
        recall = recall_score(references, predictions)
        f1 = fbeta_score(references, predictions, beta=1)
        f2 = fbeta_score(references, predictions, beta=2)
        metrics = {"precision": precision, "recall": recall, "f1": f1, "f2": f2}
        return metrics

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
