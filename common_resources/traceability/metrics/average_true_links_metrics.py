from typing import Dict

import datasets
import numpy as np

from common_resources.data.tdatasets.trace_matrix import TraceMatrix
from common_resources.traceability.metrics.abstract_trace_metric import AbstractTraceMetric

_DESCRIPTION = """
The average true links per query by source artifact.
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions (`list` of `float`): Predicted labels.
    references (`list` of `int`): Ground truth labels.
Returns:
    avg_true_links (`float` or `int`): Average true links per query.
"""

_CITATION = """
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class AverageTrueLinksMetric(AbstractTraceMetric):
    name = "avg_true_links"

    # TODO
    def _compute(self, predictions, references, trace_matrix: TraceMatrix, **kwargs) -> Dict:
        """
        Returns the average true links per query.
        :param predictions: predicted labels
        :param references: ground truth labels.
        :param trace_matrix: Matrix used to calculate trace metrics.
        :param kwargs: any other necessary params
        :return: Average number of positive links.
        """

        def get_n_positives(labels, _):
            """
            Returns the number of positive labels in query.
            :param labels: The labels in the query.
            :param _: Ignored.
            :return: The sum of labels, assuming negative label is 0.
            """
            return sum(labels)

        score = trace_matrix.calculate_query_metric(get_n_positives, default_value=np.nan)

        return {
            "avg_true_links": score
        }

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
