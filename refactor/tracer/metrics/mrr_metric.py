import datasets

from tracer.metrics.abstract_trace_metric import AbstractTraceMetric

_DESCRIPTION = """
Mean Reciprocal Rank metric measures how far down the ranking the first relevant link is
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions (`list` of `int`): Predicted labels.
    references (`list` of `int`): Ground truth labels.
Returns:
    mrr (`float` or `int`): mrr score. 
"""

_CITATION = """
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class MRRMetric(AbstractTraceMetric):

    # TODO
    def _compute(self, predictions, labels, **kwargs) -> float:
        """
        Computes the Mean Reciprocal Rank or how far down the ranking the first relevant link is
        :param predictions: predicted labels
        :param labels: ground truth labels
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
