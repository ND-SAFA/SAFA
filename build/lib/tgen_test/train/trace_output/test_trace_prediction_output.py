from tgen.core.save_strategy.comparison_criteria import ComparisonCriterion
from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.metrics.supported_trace_metric import SupportedTraceMetric
from tgen.testres.base_tests.base_test import BaseTest

PRECISION_METRIC_NAME = SupportedTraceMetric.PRECISION_AT_K.name


class TestTracePredictionOutput(BaseTest):

    def test_is_better_than(self):
        result1 = self.create_precision_output(precision_value=0.8)
        result2 = self.create_precision_output(precision_value=0.3)
        self.assertTrue(
            result1.is_better_than(result2, ComparisonCriterion(PRECISION_METRIC_NAME, "max")))
        self.assertFalse(
            result1.is_better_than(result2, ComparisonCriterion(PRECISION_METRIC_NAME, "min")))
        self.assertFalse(result2.is_better_than(result1, ComparisonCriterion(PRECISION_METRIC_NAME, "max")))

    def test_can_compare_with_metric(self):
        result1 = self.create_precision_output(precision_value=0.8)
        result2 = self.create_precision_output(precision_value=0.3)
        self.assertTrue(result1._can_compare_with_metric(result2, PRECISION_METRIC_NAME))
        self.assertFalse(result1._can_compare_with_metric(result2, None))
        self.assertFalse(result1._can_compare_with_metric(result2, "unknown_metric"))

    def test_get_comparison_vals(self):
        result1 = self.create_precision_output(precision_value=0.8)
        result2 = self.create_precision_output(precision_value=0.3)
        metric1, metric2 = result1._get_comparison_vals(result2, PRECISION_METRIC_NAME)
        self.assertEqual(metric1, 0.8)
        self.assertEqual(metric2, 0.3)

    @staticmethod
    def create_precision_output(results_dict=None, precision_value=0.8):
        if results_dict is None:
            results_dict = {"metrics": {PRECISION_METRIC_NAME: precision_value}}
        return TracePredictionOutput(**results_dict)
