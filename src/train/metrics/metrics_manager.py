import warnings
from typing import Dict, List, Tuple, Union

import numpy as np
from datasets import load_metric
from scipy.special import softmax

from data.datasets.trace_matrix import TraceMatrix
from data.tree.trace_link import TraceLink
from train.metrics.map_at_k_metric import MapAtKMetric
from train.metrics.map_metric import MapMetric
from train.metrics.precision_at_threshold_metric import PrecisionAtKMetric
from train.metrics.recall_at_threshold_metric import RecallAtThresholdMetric
from train.metrics.supported_trace_metric import get_metric_name, get_metric_path
from train.trace_output.stage_eval import Metrics, TracePredictions
from train.trace_output.trace_prediction_output import TracePredictionEntry

warnings.filterwarnings('ignore')
ArtifactQuery = Dict[str, List[TraceLink]]
ProjectQueries = Dict[str, ArtifactQuery]


class MetricsManager:
    """
    Calculates metrics for trace trainer.
    """

    def __init__(self, trace_links: List[TraceLink], trace_predictions: TracePredictions = None,
                 predicted_similarities: List[float] = None):
        """
        Constructs metrics manager with labels from trace links and scores from prediction output.
        :param trace_links: The links defining the labels associated with prediction output.
        :param trace_predictions: The output of a model.
        :param predicted_similarities: The similarity scores predicted
        """
        scores = self.get_similarity_scores(trace_predictions) if predicted_similarities is None else predicted_similarities
        self.trace_matrix = TraceMatrix(trace_links, scores)

    def eval(self, metric_names: List) -> Metrics:
        """
        Evaluates scores using metrics and adds to base metrics. (use this instead of Trainer.evaluation to utilize predefined metrics
        from models)
        :param metric_names: name of metrics desired for evaluation
        :return: a dictionary of metric_name to result
        """
        metric_paths = [get_metric_path(name) for name in metric_names]
        results = {}
        trace_matrix_metrics = [MapMetric.name, MapAtKMetric.name, PrecisionAtKMetric.name,
                                RecallAtThresholdMetric.name]
        scores = self.trace_matrix.scores
        labels = self.trace_matrix.labels
        for metric_path in metric_paths:
            metric = load_metric(metric_path, keep_in_memory=True)
            args = {"trace_matrix": self.trace_matrix} if metric.name in trace_matrix_metrics else {}

            metric_result = metric.compute(predictions=scores, references=labels, **args)
            metric_name = get_metric_name(metric)
            if isinstance(metric_result, dict):
                results.update(metric_result)
            else:
                results[metric_name] = metric_result
        return results

    def get_scores(self) -> List[float]:
        """
        :return: Returns the similarity scores of the prediction output.
        """
        return self.trace_matrix.scores

    def get_trace_predictions(self) -> List[TracePredictionEntry]:
        """
        Constructs trace predictions for trace matrix.
        :return: Trace predictions used in evaluation.
        """
        entries = []
        for score, label, source_target_pair in zip(self.trace_matrix.scores, self.trace_matrix.labels, self.trace_matrix.entries):
            entry: TracePredictionEntry = {
                **source_target_pair,
                "score": score,
                "label": label
            }
            entries.append(entry)
        return entries

    @staticmethod
    def get_similarity_scores(predictions: Union[np.ndarray, Tuple[np.ndarray]]) -> List[float]:
        """
        Transforms predictions into similarity scores.
        :param predictions: The model predictions.
        :return: List of similarity scores associated with predictions.
        """
        similarity_scores = []
        for pred_i in range(predictions.shape[0]):
            prediction = predictions[pred_i]
            similarity_scores.append(softmax(prediction)[1])
        return similarity_scores
