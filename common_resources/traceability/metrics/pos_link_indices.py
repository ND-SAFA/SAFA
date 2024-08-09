from typing import Dict

import datasets
import numpy as np
import pandas as pd

from common_resources.tools.util.dict_util import DictUtil
from common_resources.data.tdatasets.trace_matrix import TraceMatrix
from common_resources.traceability.metrics.abstract_trace_metric import AbstractTraceMetric

_DESCRIPTION = """
The True Link Indices metric measures the index at which true links in a software traceability 
system are ranked when sorted by their predictions.
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions (`list` of `float`): Predicted similarity scores between source and target artifacts.
    references (`list` of `int`): Ground truth links between source and target artifacts. 
Returns:
    indices (`list` of `int`): The indices where references == 1 in the ranked predictions. 
"""

_CITATION = ""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class PositiveLinkIndices(AbstractTraceMetric):
    name = "true_link_indices"

    def _compute(self, predictions, references, trace_matrix: TraceMatrix, **kwargs) -> Dict:
        """
        Computes the true link indices metric.
        :param predictions: Similarity scores for artifact pairs.
        :param references: The actual labels for the artifact pairs.
        :param trace_matrix: The matrix used to store and calculate trace metrics.
        """

        def compute_positive_link_indices(labels, preds) -> Dict:
            """
            Computes the indices of the positively predicted datums.
            :param labels: The labels of the data.
            :param preds: The predictions on the data.
            :return: Dictionary containing indices of positive predictions.
            """
            if 1 not in labels:
                return np.NAN
            zipped_list = list(zip(labels, preds))
            sorted_list = sorted(zipped_list, key=lambda x: x[1], reverse=True)
            sorted_labels, sorted_predictions = zip(*sorted_list)
            pos_link_indices = []
            for i, label in enumerate(sorted_labels):
                if label == 1:
                    pos_link_indices.append(i)
            return pd.Series(pos_link_indices).value_counts().to_dict()

        avg_positive_link_index = trace_matrix.calculate_query_metric(compute_positive_link_indices, joining_function=DictUtil.joining)
        avg_positive_link_index = dict(sorted(avg_positive_link_index.items(), key=lambda x: x[0]))

        return {
            "index_histogram": avg_positive_link_index
        }

    def _info(self) -> datasets.MetricInfo:
        """
        :return: The metric information.
        """
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=self.get_features(),
            reference_urls=[""],
        )
