from typing import Dict

import datasets

from common_resources.traceability.metrics.abstract_trace_metric import AbstractTraceMetric
from common_resources.traceability.metrics.confusion_matrix_at_threshold_metric import ConfusionMatrixAtThresholdMetric

_DESCRIPTION = """
Specificity metric calculates the number of true negatives over all predicted negatives.
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions (`list` of `int`): Predicted similarity scores.
    references (`list` of `int`): Ground truth labels.
Returns:
    specificity (`float` or `int`): Specificity score. 
"""

_CITATION = """
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class SpecificityMetric(AbstractTraceMetric):

    def _compute(self, predictions, references, **kwargs) -> float:
        """
        Calculates specificity (the number of true negatives over all predicted negatives).
        :param predictions: predicted labels
        :param references: ground truth labels.
        :param kwargs: any other necessary params
        :return: The specificity
        """
        matrix: Dict = ConfusionMatrixAtThresholdMetric()._compute(predictions, references, **kwargs)
        return matrix["tn"] / (matrix["tn"] + matrix["fp"])

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
