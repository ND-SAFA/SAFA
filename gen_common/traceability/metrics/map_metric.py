from typing import Dict

import datasets
from sklearn.metrics import average_precision_score

from gen_common.constants import AP_KEY, MAP_KEY, THRESHOLD_DEFAULT
from gen_common.data.tdatasets.trace_matrix import TraceMatrix
from gen_common.traceability.metrics.abstract_trace_metric import AbstractTraceMetric

_DESCRIPTION = """
Mean Average Precision@K metric measures the average precision over k for recommendations shown for 
different links and averages them over all queries in the data.
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions (`list` of `float`): Predicted labels.
    references (`list` of `int`): Ground truth labels.
    k (int): considers only the subset of recommendations from rank 1 through k
Returns:
    map (`float` or `int`): Mean Average Precision@K score. 
"""

_CITATION = """
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class MapMetric(AbstractTraceMetric):
    name = "map"

    # TODO
    def _compute(self, predictions, references, trace_matrix: TraceMatrix, k=THRESHOLD_DEFAULT,
                 **kwargs) -> Dict:
        """
        computes the Mean Average Precision@K or the average precision over k for recommendations shown for different links
         and averages them over all queries in the data.
        :param predictions: predicted labels
        :param references: ground truth labels.
        :param trace_matrix: Matrix used to calculate trace metrics.
        :param k: considers only the subset of recommendations from rank 1 through k
        :param kwargs: any other necessary params
        :return: Mean Average Precision@K score.
        """
        map_score = trace_matrix.calculate_query_metric(average_precision_score, default_value=0)
        ap_score = average_precision_score(references, predictions)
        return {
            MAP_KEY: map_score,
            AP_KEY: ap_score
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
