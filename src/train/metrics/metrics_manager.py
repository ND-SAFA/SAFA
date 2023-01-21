from typing import Dict, List, Tuple, Union

import numpy as np
from datasets import load_metric
from torch import softmax
from transformers.trainer_utils import PredictionOutput

from data.datasets.trace_matrix import TraceMatrix
from data.tree.trace_link import TraceLink
from train.metrics.map_at_k_metric import MapAtKMetric
from train.metrics.map_metric import MapMetric
from train.metrics.precision_at_threshold_metric import PrecisionAtKMetric
from train.metrics.recall_at_threshold_metric import RecallAtThresholdMetric
from train.metrics.supported_trace_metric import get_metric_name, get_metric_path
from train.trace_output.trace_output_types import Metrics

ArtifactQuery = Dict[str, List[TraceLink]]
ProjectQueries = Dict[str, ArtifactQuery]


class MetricsManager:
    """
    Contains trace and similarity matrices for computing query-based metrics.
    """

    def __init__(self, trace_links: List[TraceLink], prediction_output: PredictionOutput):
        """
        Constructs similarity and trace matrices using predictions trace_output.
        :param trace_matrix: The matrix containing similarity scores.
        """
        scores = self.get_similarity_scores(prediction_output.predictions)
        self.trace_matrix = TraceMatrix(trace_links, scores)

    def eval(self, metric_names: List) -> Metrics:
        """
        Evaluates scores using metrics and adds to base metrics. (use this instead of Trainer.evaluation to utilize predefined metrics from models)
        :param metric_names: name of metrics desired for evaluation
        :return: a dictionary of metric_name to result
        """
        metric_paths = [get_metric_path(name) for name in metric_names]
        results = {}
        trace_matrix_metrics = [MapMetric.name, MapAtKMetric.name, PrecisionAtKMetric.name,
                                RecallAtThresholdMetric.name]
        for metric_path in metric_paths:
            metric = load_metric(metric_path, keep_in_memory=True)
            args = {"trace_matrix": self} if metric.name in trace_matrix_metrics else {}
            metric_result = metric.compute(predictions=self.trace_matrix.scores, references=self.trace_matrix.labels, **args)
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
