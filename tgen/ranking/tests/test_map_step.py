from unittest import TestCase

from tgen.ranking.pipeline.classification_step import add_precision_to_metrics
from tgen.ranking.pipeline.map_step import calculate_map, calculate_map_instructions


class TestMapStep(TestCase):
    def test_map_step(self):
        predicted_target_links = [["1", "2", "3"]]
        source_ids = ["4"]
        traced_ids = ["4-2"]
        map_instructions = calculate_map_instructions(predicted_target_links, source_ids, traced_ids)

        self.assertEqual(1, len(map_instructions))
        self.assertEqual(3, map_instructions[0]["total"])
        correct_indices = map_instructions[0]["indices"]
        self.assertEqual(1, len(correct_indices))
        self.assertEqual(1, correct_indices[0])

        metrics = {}
        calculate_map(metrics, map_instructions, source_ids)
        self.assertEqual(0.5, metrics["4"]["ap"])
        self.assertEqual(0.5, metrics["base"]["map"])

        add_precision_to_metrics(metrics, map_instructions)
        self.assertEqual(0, metrics["Precision@1"])
        self.assertEqual(0.5, metrics["Precision@2"])
        self.assertEqual(1 / 3, metrics["Precision@3"])
