from typing import Dict

import datasets

from tgen.train.metrics.abstract_trace_metric import AbstractTraceMetric

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

    def _compute(self, predictions, references, **kwargs) -> Dict:
        """
        Computes the true link indices metric.
        """
        zipped_list = list(zip(references, predictions))
        sorted_list = sorted(zipped_list, key=lambda x: x[1], reverse=True)
        sorted_labels, sorted_predictions = zip(*sorted_list)
        pos_link_indices = []
        for i, label in enumerate(sorted_labels):
            if label == 1:
                pos_link_indices.append(i)
            
        return {
            "pos_indices": pos_link_indices
        }

    def _info(self) -> datasets.MetricInfo:
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=self.get_features(),
            reference_urls=[""],
        )
