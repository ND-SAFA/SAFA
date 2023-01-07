from typing import List, Tuple

import numpy as np
from sklearn.metrics import average_precision_score
from transformers.trainer_utils import PredictionOutput

from data.datasets.trace_matrix import TraceMatrixManager
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from testres.base_test import BaseTest
from train.trace_trainer import TraceTrainer


class TestTraceMatrix(BaseTest):
    THRESHOLD = 0.5
    N_TARGETS = 2
    N_SOURCES = 2
    SOURCE_ARTIFACTS = ["R1", "R2"]
    TARGET_ARTIFACTS = ["D1", "D2"]
    LABEL_IDS = [0, 1, 1, 0]
    PREDICTIONS = np.array([[0.3, 0.2], [0.3, 0.6], [0.5, 0.1], [0.1, 0.5]])
    PREDICTION_OUTPUT = PredictionOutput(label_ids=LABEL_IDS, predictions=PREDICTIONS, metrics=["map"])

    manager = None

    def setUp(self):
        self.manager = TraceMatrixManager(self.get_artifact_pairs(), TraceTrainer.get_similarity_scores(self.PREDICTIONS))

    def test_map_correctness(self) -> None:
        """
        Asserts that the correct map score is calculated.
        """

        map_score = self.manager.calculate_query_metric(average_precision_score)
        self.assertEqual(map_score, 0.75)

    def assert_matrix_sizes(self) -> None:
        """
        Assert that queries containing right number of elements.
        """
        for source in self.SOURCE_ARTIFACTS:
            source_queries = self.manager.queries[source]
            source_pred = source_queries[TraceMatrixManager.PRED_KEY]
            source_labels = source_queries[TraceMatrixManager.LINK_KEY]
            self.assertEquals(len(source_pred), self.N_TARGETS)
            self.assertEquals(len(source_labels), self.N_TARGETS)

    def assert_source_queries(self) -> None:
        """
        Asserts that source queries containing write scores and labels.
        """
        source_1 = self.SOURCE_ARTIFACTS[0]
        source_1_query = self.manager.queries[source_1]
        self.assert_query(source_1_query, [False, True], [0, 1])

        source_2 = self.SOURCE_ARTIFACTS[1]
        source_2_query = self.manager.queries[source_2]
        self.assert_query(source_2_query, [False, True], [1, 0])

    def assert_query(self, queries, expected_greater: List[bool], expected_labels: List[int]) -> None:
        """
        Asserts that queries are above or under threshold and labels have expected values.
        :param queries: Queries for source artifacts containing predictions and labels.
        :param expected_greater: List of boolean representing if score is expected to be greater than threshold.
        :param expected_labels: List of expected values.
        :return: None
        """
        predictions = queries[TraceMatrixManager.PRED_KEY]
        labels = queries[TraceMatrixManager.LINK_KEY]
        for i in range(self.N_TARGETS):
            assertion = self.assertGreater if expected_greater[i] else self.assertLess
            assertion(predictions[i], self.THRESHOLD)
            self.assertEqual(labels[i], expected_labels[i])

    def get_artifact_pairs(self) -> List[TraceLink]:
        """
        Returns list of tuples for each combination of source and target artifacts.
        :return: List of tuples containing artifact ids.
        """
        pairs = []
        i = 0
        for source_artifact in self.SOURCE_ARTIFACTS:
            for target_artifact in self.TARGET_ARTIFACTS:
                pairs.append(TraceLink(Artifact(source_artifact, "token"), Artifact(target_artifact, "token"),
                                       is_true_link=bool(self.LABEL_IDS[i])))
                i += 1
        return pairs

    def test_map(self):
        pass  # TODO: Where did this go??

    def test_metric_at_k(self):
        for k in range(1, 3, 1):
            def metric_creator(k):
                def metric(labels, preds):
                    self.assertEqual(len(labels), k)
                    self.assertEqual(len(preds), k)
                    return labels[0]

                return metric

            metric_value = self.manager.calculate_query_metric_at_k(metric_creator(k), k)
            self.assertEqual(metric_value, 0.5)
