import numpy as np
from transformers.trainer_utils import PredictionOutput

from data.datasets.trace_matrix import TraceMatrixManager
from testres.base_test import BaseTest
from train.metrics.precision_at_threshold_metric import PrecisionAtKMetric


class TestPrecisionAtKMetric(BaseTest):
    def test_correctness(self):
        """
        Tests that precision score accurately returns expected metrics.
        ---
        Predictions: 1, 1, 1
        Labels: 1, 0, 1
        Precision: tp / tp + fp
        ---
        If k = 1 then 1 / (1 + 0) = 1 / 1
        If k = 2 then 1 / (1 + 1) = 1 / 2
        If k = 3 then 1 / (2 + 1) = 1 / 3
        """
        predictions = np.array([self.create_prediction(0.6),
                                self.create_prediction(0.7),
                                self.create_prediction(0.8)
                                ])
        references = np.array([1, 0, 1, 0, 1, 0])
        source_target_pairs = [("S1", "T1"), ("S1", "T2"), ("S1", "T3")]
        output = PredictionOutput(predictions, references, [])
        trace_matrix = TraceMatrixManager(source_target_pairs, output)

        metric = PrecisionAtKMetric()
        score = metric._compute(predictions, references, trace_matrix)
        self.assertAlmostEqual(score["precision@1"], 1)
        self.assertAlmostEqual(score["precision@2"], 1 / 2)
        self.assertAlmostEqual(score["precision@3"], 2 / 3)

    @staticmethod
    def create_prediction(score: float):
        """
        Creates the prediction for wanted softmax score.
        :param score: The score desired after softmax applied to prediction.
        :return: List of tuples representing prediction per class.
        """
        positive_score = score
        negative_score = 1 - score
        return [negative_score, positive_score]
