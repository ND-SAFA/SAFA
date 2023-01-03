from typing import Callable, List, Tuple, Union

import numpy as np
from scipy.special import softmax
from transformers.trainer_utils import PredictionOutput


class TraceMatrix:
    """
    Contains trace and similarity matrices for computing query-based metrics.
    """

    def __init__(self, source_target_pairs: List[Tuple], output: PredictionOutput):
        """
        Constructs similarity and trace matrices using predictions output.
        :param source_target_pairs: The pairs of artifact represented by the predictions.
        :param output: The prediction output on the source-target pairs.
        """
        self.source_target_pairs = source_target_pairs
        self.scores = self.get_similarity_scores(output.predictions)
        similarity_matrix, trace_matrix = self.create_trace_matrix(source_target_pairs, self.scores, output.label_ids)
        self.similarity_matrix = similarity_matrix
        self.trace_matrix = trace_matrix

    def calculate_query_metric(self, metric: Callable[[List[float], List[int]], float]):
        """
        Calculates the average metric for each source artifact in project.
        :param metric: The metric to compute for each query in matrix.
        :return: Average metric value.
        """
        source_matrix = self.similarity_matrix
        trace_matrix = self.trace_matrix
        n_sources = source_matrix.shape[0]
        metric_values = []
        for source_index in range(n_sources):
            query_predictions = source_matrix[source_index, :]
            query_labels = trace_matrix[source_index, :]
            query_map = metric(query_labels, query_predictions)
            metric_values.append(query_map)
        return sum(metric_values) / len(metric_values)

    @staticmethod
    def create_trace_matrix(artifact_pairs: List[Tuple[str, str]], scores: List[float], labels: List[int]) -> Tuple[
        np.array, np.array]:
        """
        Creates similarity and trace matrices from scores and labels.
        :param artifact_pairs: The pairs of artifact corresponding to scores.
        :param scores: The similarity scores between artifacts in pairs.
        :param labels: The labels representing if the artifact pair is traced or not.
        :return: SimilarityMatrix, TraceMatrix
        """
        source_artifacts = []
        target_artifacts = []
        queries = {}
        for (source, target), score, label in zip(artifact_pairs, scores, labels):
            if source not in source_artifacts:
                source_artifacts.append(source)
            if target not in target_artifacts:
                target_artifacts.append(target)
            if source in queries:
                assert target not in queries[source]
                queries[source][target] = [score, label]
            else:
                queries[source] = {target: [score, label]}
        similarity_matrix = np.zeros((len(source_artifacts), len(target_artifacts)))
        trace_matrix = np.zeros((len(source_artifacts), len(target_artifacts)))

        for source, targets in queries.items():
            source_index = source_artifacts.index(source)
            for target, payload in targets.items():
                score, label = payload
                target_index = target_artifacts.index(target)
                similarity_matrix[source_index][target_index] = score
                trace_matrix[source_index][target_index] = label
        return similarity_matrix, trace_matrix

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
