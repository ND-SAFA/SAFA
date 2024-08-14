from typing import Dict

import datasets
from sklearn.metrics import precision_score

from common_resources.tools.constants.metric_constants import K_METRIC_DEFAULT
from common_resources.data.tdatasets.trace_matrix import TraceMatrix
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
class PrecisionAtKMetric(AbstractTraceMetric):
    name = "precision@k"

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
        results = {}

        def precision(labels, preds, label: int = 1):
            """
            Calculates the precision of predicting true for all predictions.
            :param labels: The labels defining if true labels are accurate.
            :param preds: The predictions used to calculate how many 1 to set.
            :param label: The label to set for the prediction.
            :return: The precision of predicting all of the same label for predictions.
            """
            return precision_score(labels, [label] * len(preds))

        for k in K_METRIC_DEFAULT:
            score = trace_matrix.calculate_query_metric_at_k(precision, k)
            metric_name = self.name.replace("k", str(k))
            results[metric_name] = round(score, 3)
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
