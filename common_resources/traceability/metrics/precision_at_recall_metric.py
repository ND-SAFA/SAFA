from typing import Dict

import datasets
from sklearn.metrics import precision_recall_curve

from common_resources.tools.constants.metric_constants import THRESHOLD_DEFAULT, UPPER_RECALL_THRESHOLD
from common_resources.tools.t_logging.logger_manager import logger
from common_resources.traceability.metrics.abstract_trace_metric import AbstractTraceMetric

_DESCRIPTION = """
Calculates the optimal threshold for predictions.
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions (`list` of `float`): Predicted labels.
    references (`list` of `int`): Ground truth labels.
    k (int): considers only the subset of recommendations from rank 1 through k
Returns:
    threshold (`float`): Mean Average Precision@K score. 
"""

_CITATION = """
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class PrecisionAtRecallMetric(AbstractTraceMetric):
    name = "precision_at_recall"

    # TODO
    def _compute(self, predictions, references, k=THRESHOLD_DEFAULT, **kwargs) -> Dict:
        """
        computes the Mean Average Precision@K or the average precision over k for recommendations shown for different links
         and averages them over all queries in the dataset.
        :param predictions: predicted labels
        :param references: ground truth labels.
        :param k: considers only the subset of recommendations from rank 1 through k
        :param kwargs: any other necessary params
        :return: Mean Average Precision@K score.
        """
        precisions, recalls, thresholds = precision_recall_curve(references, predictions)

        max_precision = 0
        threshold = None
        for index in range(len(recalls) - 1):
            t = thresholds[index]
            p = precisions[index]
            r = recalls[index]
            if r >= UPPER_RECALL_THRESHOLD and p > max_precision:
                threshold = t
                max_precision = p

        if threshold is None:
            logger.warning(f"Could not find threshold under {UPPER_RECALL_THRESHOLD} recall.")
        return {"precision_at_recall": max_precision, "best_threshold": threshold}

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
