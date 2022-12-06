import datasets
from sklearn.metrics import precision_score

from config.constants import K_METRIC_DEFAULT
from train.metrics.abstract_trace_metric import AbstractTraceMetric

_DESCRIPTION = """
Precision@K metric measures the percentage of predicted links that were correct.
"""

_KWARGS_DESCRIPTION = """
Args:
    predictions (`list` of `int`): Predicted labels.
    references (`list` of `int`): Ground truth labels.
    k (int): The level of the threshold to consider a similar score a true label.
Returns:
    precision_at_k (`float` or `int`): Precision@K score. 
"""

_CITATION = """
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class PrecisionAtKMetric(AbstractTraceMetric):

    # TODO
    def _compute(self, predictions, references, k=K_METRIC_DEFAULT, **kwargs) -> float:
        """
        Computes the Precision@K or the percentage of links that were correctly predicted
        :param predictions: predicted labels
        :param labels: ground truth labels.
        :param k: considers only the subset of recommendations from rank 1 through k
        :param kwargs: any other necessary params
        :return: Precision@K score.
        """
        predicted_labels = [1 if p >= k else 0 for p in predictions]
        print(self.count_errors(references, predicted_labels))
        return precision_score(references, predicted_labels)

    @staticmethod
    def count_errors(y_true, y_pred):
        errors = {
            "tp": 0,
            "tn": 0,
            "fn": 0,
            "fp": 0,
        }
        for label, pred in zip(y_true, y_pred):
            if label == pred:
                if label == 1:
                    errors["tp"] += 1
                else:
                    errors["tn"] += 1
            else:
                if label == 1:
                    errors["fn"] += 1
                else:
                    errors["fp"] += 1
        return errors

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
