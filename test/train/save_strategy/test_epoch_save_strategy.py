from typing import Dict

from tgen.core.save_strategy.comparison_criteria import ComparisonCriterion
from tgen.core.save_strategy.metric_save_strategy import MetricSaveStrategy
from tgen.core.save_strategy.save_strategy_stage import SaveStrategyStage
from tgen.testres.base_tests.base_test import BaseTest


class TestMetricSaveStrategy(BaseTest):
    """
    Tests that save strategy alerts thread when to save correctly and the comparison
    between metrics to decide best.
    """

    def test_should_evaluate(self):
        """
        Tests that epochs are triggered while steps are not.
        :return:
        """
        comparison_criteria = ComparisonCriterion(["map", "f2"])
        save_strategy = MetricSaveStrategy(comparison_criteria)
        self.assertFalse(save_strategy.should_evaluate(SaveStrategyStage.STEP, 0))
        self.assertTrue(save_strategy.should_evaluate(SaveStrategyStage.EPOCH, 0))

    def test_should_save(self):
        """
        Verifies that is better correctly integrates multi-metric comparisons.
        """
        comparison_criteria = ComparisonCriterion(["map", "f2"])
        save_strategy = MetricSaveStrategy(comparison_criteria)
        entry_0 = {"map": 0.6, "f2": 0.4}

        eval_entries = save_strategy.stage_evaluations

        def assert_entry(test_entry: Dict, i: int):
            is_better = save_strategy.should_save(entry_0, i)
            self.assertTrue(is_better)
            self.assertEqual(i + 1, len(eval_entries))
            self.assertDictEqual(test_entry, eval_entries[i])

        assert_entry(entry_0, 0)

        for i, m in enumerate(zip(entry_0.keys(), [])):
            # iter 1: map = 0.7, f2 = 0.4 -> Beat first.
            # iter 2: f2 = 0.7, f2 = 0.7 -> Tied first, beat second.
            new_entry = {**entry_0, m: 0.7}
            assert_entry(new_entry, i + 1)  # iteration 0 already processed

        self.assertFalse(save_strategy.should_save(entry_0, 3))
