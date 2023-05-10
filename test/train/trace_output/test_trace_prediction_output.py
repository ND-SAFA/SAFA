from tgen.testres.base_tests.base_test import BaseTest
from tgen.train.metrics.supported_trace_metric import SupportedTraceMetric
from tgen.train.save_strategy.comparison_criteria import ComparisonCriterion
from tgen.train.trace_output.trace_prediction_output import TracePredictionOutput


class TestTracePredictionOutput(BaseTest):

    def test_is_better_than(self):
        result1 = self.get_prediction_output(precision_at_k=0.8)
        result2 = self.get_prediction_output(precision_at_k=0.3)
        self.assertTrue(
            result1.is_better_than(result2, ComparisonCriterion("precision", "max")))
        self.assertFalse(
            result1.is_better_than(result2, ComparisonCriterion("precision", "min")))
        self.assertFalse(result2.is_better_than(result1, ComparisonCriterion("precision", "max")))

    def test_can_compare_with_metric(self):
        result1 = self.get_prediction_output(precision_at_k=0.8)
        result2 = self.get_prediction_output(precision_at_k=0.3)
        self.assertTrue(result1._can_compare_with_metric(result2, SupportedTraceMetric.PRECISION.name))
        self.assertFalse(result1._can_compare_with_metric(result2, None))
        self.assertFalse(result1._can_compare_with_metric(result2, "precision_at_k"))

    def test_get_comparison_vals(self):
        result1 = self.get_prediction_output(precision_at_k=0.8)
        result2 = self.get_prediction_output(precision_at_k=0.3)
        metric1, metric2 = result1._get_comparison_vals(result2, SupportedTraceMetric.PRECISION.name)
        self.assertEquals(metric1, 0.8)
        self.assertEquals(metric2, 0.3)

    def get_prediction_output(self, results_dict=None, precision_at_k=0.8):
        if results_dict is None:
            results_dict = {"metrics": {SupportedTraceMetric.PRECISION.name: precision_at_k}}
        return TracePredictionOutput(**results_dict)
