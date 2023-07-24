from typing import Dict

import datasets

from tgen.constants.metric_constants import THRESHOLD_DEFAULT
from tgen.metrics.abstract_trace_metric import AbstractTraceMetric

_DESCRIPTION = """
Confusion matrix metric calculates the number of true and false positives and the true/false negatives.
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions (`list` of `int`): Predicted similarity scores.
    references (`list` of `int`): Ground truth labels.
    k (int): The level of the threshold to consider a similar score a true label.
Returns:
    precision_at_k (`float` or `int`): Precision@K score. 
"""

_CITATION = """
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class ConfusionMatrixAtThresholdMetric(AbstractTraceMetric):

    def _compute(self, predictions, references, k=THRESHOLD_DEFAULT, **kwargs) -> Dict[str, float]:
        """
        Confusion matrix metric calculates the number of true and false positives and the true/false negatives.
        :param predictions: predicted labels
        :param labels: ground truth labels.
        :param k: considers only the subset of recommendations from rank 1 through k
        :param kwargs: any other necessary params
        :return: Dictionary containing counts for the different results.
        """
        predicted_labels = [1 if p >= k else 0 for p in predictions]
        return self.calculate_confusion_matrix(references, predicted_labels)

    @staticmethod
    def calculate_confusion_matrix(y_true, y_pred):
        errors = {
            "tp": 0,
            "tn": 0,
            "fn": 0,
            "fp": 0,
        }
        for label, pred in zip(y_true, y_pred):
            if label == pred:
                if label == 1:
                    errors["tp"] += 1
                else:
                    errors["tn"] += 1
            else:
                if pred == 1:
                    errors["fp"] += 1
                else:
                    errors["fn"] += 1
        return errors

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
