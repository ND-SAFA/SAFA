from unittest import TestCase

from tgen.experiments.ensemble_experiment import EnsembleExperiment


class TestEnsembleExperiment(TestCase):
    """
    Tests the correctness of scores aggregation.
    """

    def test_link_aggregation(self):
        """
        Tests that links are aggregated across techniques.
        """
        predictions = [[0.1, 0.2, 0.4], [0.1, 0.2, 0.4]]
        aggregated_scores = EnsembleExperiment.ensemble_predictions(predictions, sum)
        self.assertEqual(3, len(aggregated_scores))
        self.assertEqual(0.2, aggregated_scores[0])
        self.assertEqual(0.4, aggregated_scores[1])
        self.assertEqual(0.8, aggregated_scores[2])

    def test_scale_predictions(self):
        """
        Tests that distribution with the same variance lead to the same scores.
        """
        predictions = [[1.1, 1.2, 1.3], [0.1, 0.2, 0.3]]
        scaled_scores = EnsembleExperiment.scale_predictions(predictions)
