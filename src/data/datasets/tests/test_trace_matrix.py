import numpy as np
from transformers.trainer_utils import PredictionOutput

from data.datasets.trace_matrix import TraceMatrix
from testres.base_test import BaseTest


class TestTraceMatrix(BaseTest):
    def test_matrix_construction(self):
        labels_ids = [0, 1, 0]
        predictions = np.array([[0.3, 0.2], [0.3, 0.6], [0.5, 0.1]])
        output = PredictionOutput(label_ids=labels_ids, predictions=predictions, metrics=["map"])
        artifact_pairs = [("R1", "R4"), ("R2", "R4"), ("R3", "R4")]
        trace_matrix = TraceMatrix(artifact_pairs, output)
        similarity_matrix = trace_matrix.similarity_matrix
        trace_matrix = trace_matrix.trace_matrix

        # Assert matrix sizes
        for matrix in [similarity_matrix, trace_matrix]:
            n_sources = matrix.shape[0]
            n_targets = matrix.shape[1]
            self.assertEquals(n_sources, 3)
            self.assertEquals(n_targets, 1)

        # Assert similarity
        self.assertLess(similarity_matrix[0][0], 0.5)
        self.assertGreater(similarity_matrix[1][0], 0.5)
        self.assertLess(similarity_matrix[2][0], 0.5)

        # Assert labels
        self.assertEqual(trace_matrix[0][0], 0)
        self.assertEqual(trace_matrix[1][0], 1)
        self.assertEqual(trace_matrix[2][0], 0)
