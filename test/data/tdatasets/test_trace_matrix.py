from typing import List

import numpy as np
from sklearn.metrics import average_precision_score
from transformers.trainer_utils import PredictionOutput

from tgen.data.tdatasets.trace_matrix import TraceMatrix
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.testres.base_tests.base_test import BaseTest
from tgen.train.metrics.metrics_manager import MetricsManager


class TestTraceMatrix(BaseTest):
    THRESHOLD = 0.5
    N_TARGETS = 2
    N_SOURCES = 2
    SOURCE_ARTIFACTS = ["R1", "R2"]
    TARGET_ARTIFACTS = ["D1", "D2"]
    LABEL_IDS = [0, 1, 1, 0]
    PREDICTIONS = np.array([[0.3, 0.2], [0.3, 0.6], [0.5, 0.1], [0.1, 0.5]])
    PREDICTION_OUTPUT = PredictionOutput(label_ids=LABEL_IDS, predictions=PREDICTIONS, metrics=["map"])

    trace_matrix = None

    def setUp(self):
        trace_df, link_ids = self.get_trace_df()
        self.trace_matrix = TraceMatrix(trace_df, MetricsManager.get_similarity_scores(self.PREDICTIONS), link_ids)

    def test_map_correctness(self) -> None:
        """
        Asserts that the correct map score is calculated.
        """

        map_score = self.trace_matrix.calculate_query_metric(average_precision_score)
        self.assertEqual(map_score, 0.75)

    def test_matrix_sizes(self) -> None:
        """
        Assert that queries containing right number of elements.
        """
        for source in self.SOURCE_ARTIFACTS:
            source_queries = self.trace_matrix.query_matrix[source]
            source_pred = source_queries.preds
            source_labels = source_queries.links
            self.assertEquals(len(source_pred), self.N_TARGETS)
            self.assertEquals(len(source_labels), self.N_TARGETS)
        self.assertEquals(len(self.trace_matrix.source_ids), len(self.SOURCE_ARTIFACTS))

    def test_source_queries(self) -> None:
        """
        Asserts that source queries containing write scores and labels.
        """
        source_1 = self.SOURCE_ARTIFACTS[0]
        source_1_query = self.trace_matrix.query_matrix[source_1]
        self.assert_query(source_1_query, [False, True], [0, 1])

        source_2 = self.SOURCE_ARTIFACTS[1]
        source_2_query = self.trace_matrix.query_matrix[source_2]
        self.assert_query(source_2_query, [False, True], [1, 0])

    def assert_query(self, queries, expected_greater: List[bool], expected_labels: List[int]) -> None:
        """
        Asserts that queries are above or under threshold and labels have expected values.
        :param queries: Queries for source artifacts containing predictions and labels.
        :param expected_greater: List of boolean representing if score is expected to be greater than threshold.
        :param expected_labels: List of expected values.
        :return: None
        """
        predictions = queries.preds
        links = queries.links
        for i in range(self.N_TARGETS):
            assertion = self.assertGreater if expected_greater[i] else self.assertLess
            assertion(predictions[i], self.THRESHOLD)
            self.assertEqual(links[i][TraceKeys.LABEL], expected_labels[i])

    def get_trace_df(self) -> List[TraceDataFrame]:
        """
        Returns list of tuples for each combination of source and target artifacts.
        :return: List of tuples containing artifact ids.
        """
        links = {TraceKeys.SOURCE.value: [], TraceKeys.TARGET.value: [], TraceKeys.LABEL.value: []}
        link_ids = []
        i = 0
        for source_artifact in self.SOURCE_ARTIFACTS:
            for target_artifact in self.TARGET_ARTIFACTS:
                links[TraceKeys.SOURCE.value].append(source_artifact)
                links[TraceKeys.TARGET.value].append(target_artifact)
                links[TraceKeys.LABEL.value].append(self.LABEL_IDS[i])
                link_ids.append(TraceDataFrame.generate_link_id(source_artifact, target_artifact))
                i += 1
        return TraceDataFrame(links), link_ids

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

            metric_value = self.trace_matrix.calculate_query_metric_at_k(metric_creator(k), k)
            self.assertEqual(metric_value, 0.5)
