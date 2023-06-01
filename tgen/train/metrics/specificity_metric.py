from typing import Dict

from tgen.train.metrics.abstract_trace_metric import AbstractTraceMetric

import datasets

from tgen.constants.metric_constants import THRESHOLD_DEFAULT
from tgen.train.metrics.abstract_trace_metric import AbstractTraceMetric
from tgen.train.metrics.confusion_matrix_at_threshold_metric import ConfusionMatrixAtThresholdMetric

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
class SpecificityMetric(AbstractTraceMetric):

    def _compute(self, predictions, references, **kwargs) -> float:
        """
        Confusion matrix metric calculates the number of true and false positives and the true/false negatives.
        :param predictions: predicted labels
        :param labels: ground truth labels.
        :param k: considers only the subset of recommendations from rank 1 through k
        :param kwargs: any other necessary params
        :return: Dictionary containing counts for the different results.
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
