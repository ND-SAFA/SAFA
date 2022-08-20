from trace.metrics.abstract_trace_metric import AbstractTraceMetric
from trace.config.constants import K_METRIC_DEFAULT
import datasets


_DESCRIPTION = """
Precision@K metric measures the percentage of links that were correctly predicted
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions (`list` of `int`): Predicted labels.
    references (`list` of `int`): Ground truth labels.
    k (int): considers only the subset of recommendations from rank 1 through k
Returns:
    precision_at_k (`float` or `int`): Precision@K score. 
"""

_CITATION = """
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class PrecisionAtKMetric(AbstractTraceMetric):
    metric_name = "precision_at_k"

    # TODO
    def _perform_compute(self, predictions, labels, k=K_METRIC_DEFAULT, **kwargs) -> float:
        """
        Computes the Precision@K or the percentage of links that were correctly predicted
        :param predictions: predicted labels
        :param labels: ground truth labels.
        :param k: considers only the subset of recommendations from rank 1 through k
        :param kwargs: any other necessary params
        :return: Precision@K score.
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
