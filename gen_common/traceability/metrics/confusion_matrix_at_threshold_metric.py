from typing import Dict, List

import datasets

from gen_common.constants.metric_constants import THRESHOLD_DEFAULT
from gen_common.traceability.metrics.abstract_trace_metric import AbstractTraceMetric
from gen_common.util.enum_util import EnumDict
from gen_common.util.metrics_util import MetricsUtil
from gen_common.util.supported_enum import SupportedEnum

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


class ErrorLabel(SupportedEnum):
    TP = "tp"
    TN = "tn"
    FP = "fp"
    FN = "fn"


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class ConfusionMatrixAtThresholdMetric(AbstractTraceMetric):

    def _compute(self, predictions, references, scores=None, k=THRESHOLD_DEFAULT, **kwargs) -> Dict[str, float]:
        """
        Confusion matrix metric calculates the number of true and false positives and the true/false negatives.
        :param predictions: predicted labels
        :param references: ground truth labels.
        :param scores: Contains the continuous values predicting the strength of the label.
        :param k: considers only the subset of recommendations from rank 1 through k
        :param kwargs: any other necessary params
        :return: Dictionary containing counts for the different results.
        """
        scores = scores if scores else predictions
        predicted_labels = scores if MetricsUtil.has_labels(scores) else [1 if p >= k else 0 for p in scores]
        return self.calculate_confusion_matrix(references, predicted_labels)

    @staticmethod
    def calculate_confusion_matrix(y_true: List[float], y_pred: List[float]):
        """
        Computes confusion matrix between actual and predicted labels.
        :param y_true: List of true labels.
        :param y_pred: List of predicted labels
        :return: Dictionary containing number of true positives, true negatives, false positives, and false negatives.
        """
        errors = EnumDict({label: 0 for label in ErrorLabel})

        for label, pred in zip(y_true, y_pred):
            if label == pred:
                if label == 1:
                    errors[ErrorLabel.TP] += 1
                else:
                    errors[ErrorLabel.TN] += 1
            else:
                if pred == 1:
                    errors[ErrorLabel.FP] += 1
                else:
                    errors[ErrorLabel.FN] += 1
        return dict(errors)

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
