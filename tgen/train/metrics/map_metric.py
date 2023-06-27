from typing import Dict

import datasets
from sklearn.metrics import average_precision_score

from tgen.constants.metric_constants import THRESHOLD_DEFAULT
from tgen.data.tdatasets.trace_matrix import TraceMatrix
from tgen.train.metrics.abstract_trace_metric import AbstractTraceMetric

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
    MAP_KEY = "map"
    AP_KEY = "ap"

    # TODO
    def _compute(self, predictions, references, trace_matrix: TraceMatrix, k=THRESHOLD_DEFAULT,
                 **kwargs) -> Dict:
        """
        computes the Mean Average Precision@K or the average precision over k for recommendations shown for different links
         and averages them over all queries in the data.
        :param predictions: predicted labels
        :param labels: ground truth labels.
        :param k: considers only the subset of recommendations from rank 1 through k
        :param kwargs: any other necessary params
        :return: Mean Average Precision@K score.
        """

        def print_pos_link_indices() -> None:
            zipped_list = list(zip(references, predictions))
            sorted_list = sorted(zipped_list, key=lambda x: x[1], reverse=True)
            sorted_labels, sorted_predictions = zip(*sorted_list)
            pos_link_indices = []
            for i, label in enumerate(sorted_labels):
                if label == 1:
                    pos_link_indices.append(i)
            print("Indices:", pos_link_indices)

        print_pos_link_indices()
        map_score = trace_matrix.calculate_query_metric(average_precision_score, default_value=0)
        ap_score = average_precision_score(references, predictions)
        return {
            self.MAP_KEY: map_score,
            self.AP_KEY: ap_score
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
