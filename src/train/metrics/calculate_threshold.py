import datasets
from sklearn.metrics import precision_recall_curve

from config.constants import K_METRIC_DEFAULT
from train.metrics.abstract_trace_metric import AbstractTraceMetric

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
class CalculateThreshold(AbstractTraceMetric):
    metric_name = "threshold"
    UPPER_RECALL_THRESHOLD = .95

    # TODO
    def _perform_compute(self, predictions, labels, k=K_METRIC_DEFAULT, **kwargs) -> float:
        """
        computes the Mean Average Precision@K or the average precision over k for recommendations shown for different links
         and averages them over all queries in the dataset.
        :param predictions: predicted labels
        :param labels: ground truth labels.
        :param k: considers only the subset of recommendations from rank 1 through k
        :param kwargs: any other necessary params
        :return: Mean Average Precision@K score.
        """
        precisions, recalls, thresholds = precision_recall_curve(labels, predictions)

        max_precision = 0
        threshold = None
        for index in range(len(recalls) - 1):
            t = thresholds[index]
            p = precisions[index]
            r = recalls[index]
            if r >= self.UPPER_RECALL_THRESHOLD and p > max_precision:
                print("(T, P, R)", "(%s, %s, %s)" % (t, p, r))
                threshold = t

        if threshold is None:
            print("Could not find threshold under ", self.UPPER_RECALL_THRESHOLD, " recall.")
            threshold = 0.5
        return threshold

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
