from typing import Dict, List

import datasets
import numpy as np

from gen_common.constants.metric_constants import LAG_KEY, THRESHOLD_DEFAULT
from gen_common.data.tdatasets.trace_matrix import TraceMatrix
from gen_common.traceability.metrics.abstract_trace_metric import AbstractTraceMetric

_DESCRIPTION = """
LAG measures the number of false positives necessary to read 
as an analyst before encountering all true positives.
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions (`list` of `float`): Predicted references.
    references (`list` of `int`): Ground truth references.
Returns:
    lag (`float` or `int`): Average lag score per source query. 
"""

_CITATION = """
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class LagMetric(AbstractTraceMetric):
    name = "lag"

    # TODO
    def _compute(self, predictions, references, trace_matrix: TraceMatrix, k=THRESHOLD_DEFAULT,
                 **kwargs) -> Dict:
        """
        computes the Mean Average Precision@K or the average precision over k for recommendations shown for different links
         and averages them over all queries in the data.
        :param predictions: predicted references
        :param references: ground truth references.
        :param trace_matrix: Matrix used to calculate query-based trace metrics.
        :param k: considers only the subset of recommendations from rank 1 through k
        :param kwargs: any other necessary params
        :return: Mean Average Precision@K score.
        """

        def lag_counter(labels: List[int], scores: List[float]):
            """
            Counters the number of false-positives before encountering all true-positives.
            :param labels: Ground truth traces, either 1 or 0.
            :param scores: The similarities scores for a given technique.
            :return: The lag score per query.
            """
            sorted_traces = zip(labels, scores)
            sorted_traces = sorted(sorted_traces, key=lambda x: x[1], reverse=True)
            true_trace_indices = [i for i, t in enumerate(sorted_traces) if t[0] == 1]

            if len(true_trace_indices) == 0:
                return np.nan

            n_analyzed = max(true_trace_indices) + 1
            return n_analyzed

        lag_score = trace_matrix.calculate_query_metric(lag_counter, default_value=None)
        return {
            LAG_KEY: lag_score
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
