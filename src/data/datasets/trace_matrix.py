from typing import Callable, Dict, List, Tuple, Union

import numpy as np
from scipy.special import softmax
from transformers.trainer_utils import PredictionOutput

ArtifactQuery = Dict[str, List[float]]
ProjectQueries = Dict[str, ArtifactQuery]


class TraceMatrixManager:
    PRED_KEY = "preds"
    LABEL_KEY = "labels"
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
        self.queries = self.create_trace_matrix(source_target_pairs, self.scores, output.label_ids)

    def calculate_query_metric(self, metric: Callable[[List[float], List[int]], float]):
        """
        Calculates the average metric for each source artifact in project.
        :param metric: The metric to compute for each query in matrix.
        :return: Average metric value.
        """
        metric_values = []
        for source, query in self.queries.items():
            query_predictions = query[self.PRED_KEY]
            query_labels = query[self.LABEL_KEY]
            query_map = metric(query_labels, query_predictions)
            print("-" * 15)
            results = list(zip(query_labels, query_predictions))
            res = sorted(results, key=lambda x: x[1], reverse=True)
            print(res)
            print(query_map)
            if not np.isnan(query_map):
                metric_values.append(query_map)
        return sum(metric_values) / len(metric_values)

    @staticmethod
    def create_trace_matrix(artifact_pairs: List[Tuple[str, str]], scores: List[float], labels: List[int]) -> Dict:
        """
        Creates similarity and trace matrices from scores and labels.
        :param artifact_pairs: The pairs of artifact corresponding to scores.
        :param scores: The similarity scores between artifacts in pairs.
        :param labels: The labels representing if the artifact pair is traced or not.
        :return: SimilarityMatrix, TraceMatrix
        """
        queries: ProjectQueries = {}
        for (source, target), pred, label in zip(artifact_pairs, scores, labels):
            if source in queries:
                assert target not in queries[source]
                queries[source][TraceMatrixManager.PRED_KEY].append(pred)
                queries[source][TraceMatrixManager.LABEL_KEY].append(label)
            else:
                queries[source] = {
                    TraceMatrixManager.PRED_KEY: [pred],
                    TraceMatrixManager.LABEL_KEY: [label]
                }
        return queries

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
