import datasets
from sklearn.metrics import recall_score

from config.constants import K_METRIC_DEFAULT
from train.metrics.abstract_trace_metric import AbstractTraceMetric

_DESCRIPTION = """
Recall@K metric measures the percentage of true links that were correctly predicted.
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions (`list` of `int`): Predicted labels.
    references (`list` of `int`): Ground truth labels.
    k (int): The level of the threshold to consider a similar score a true label.
Returns:
    recall_at_k (`float` or `int`): Recall@K score. 
"""

_CITATION = """
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class RecallAtThresholdMetric(AbstractTraceMetric):

    # TODO
    def _compute(self, predictions, references, k=K_METRIC_DEFAULT, **kwargs) -> float:
        """
        Recall@K metric measures the percentage of true links that were correctly predicted.
        :param predictions: predicted labels
        :param labels: ground truth labels.
        :param k: considers only the subset of recommendations from rank 1 through k
        :param kwargs: any other necessary params
        :return: Recall@K score.
        """
        predicted_labels = [1 if p >= k else 0 for p in predictions]
        return recall_score(references, predicted_labels)

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
