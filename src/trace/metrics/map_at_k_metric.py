from trace.metrics.abstract_trace_metric import AbstractTraceMetric
from trace.config.constants import K_METRIC_DEFAULT
import datasets

_DESCRIPTION = """
Mean Average Precision@K metric measures the average precision over k for recommendations shown for 
different links and averages them over all queries in the dataset.
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions (`list` of `int`): Predicted labels.
    references (`list` of `int`): Ground truth labels.
    k (int): considers only the subset of recommendations from rank 1 through k
Returns:
    map_at_k (`float` or `int`): Mean Average Precision@K score. 
"""

_CITATION = """
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class MapAtKMetric(AbstractTraceMetric):
    metric_name = "map_at_k"

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
        return 0

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
