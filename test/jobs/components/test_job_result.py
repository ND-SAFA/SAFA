import json

from tgen.jobs.components.job_result import JobResult
from tgen.testres.base_tests.base_test import BaseTest
from tgen.train.metrics.supported_trace_metric import SupportedTraceMetric
from tgen.train.save_strategy.comparison_criteria import ComparisonCriterion
from tgen.train.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.util.status import Status


class TestJobResult(BaseTest):

    def test_set_get_job_status(self):
        result = self.get_job_result()
        self.assertEquals(result.get_job_status(), Status.UNKNOWN)
        result.set_job_status(Status.SUCCESS)
        self.assertEquals(result.get_job_status(), Status.SUCCESS)

    def test_update(self):
        result1 = self.get_job_result()
        result2 = self.get_job_result({JobResult.STATUS: 1})
        result1.update(result2)
        result1[JobResult.BODY][TracePredictionOutput.PREDICTIONS] = [{"source": "s1", "target": "t2", "score": 0.9}]
        self.assertIn(TracePredictionOutput.METRICS.upper(), result1[JobResult.BODY])
        self.assertIn(SupportedTraceMetric.PRECISION.name.lower(),  result1[JobResult.BODY][TracePredictionOutput.METRICS])
        self.assertIn(JobResult.STATUS, result1)
        self.assertEquals(result1[JobResult.STATUS], 1)
        self.assertIn(TracePredictionOutput.PREDICTIONS, result1[JobResult.BODY])

    def test_to_json_and_from_dict(self):
        result1 = self.get_job_result()
        json_result = result1.to_json()
        result2 = JobResult.from_dict(json.loads(json_result))
        self.assertEquals(result1, result2)

    def test_as_dict_and_from_dict(self):
        result1 = self.get_job_result()
        result_dict = result1.as_dict()
        result2 = JobResult.from_dict(result_dict)
        self.assertEquals(result1, result2)

    def test_is_better_than(self):
        result1 = self.get_job_result(precision_at_k=0.8)
        result2 = self.get_job_result(precision_at_k=0.3)
        self.assertTrue(
            result1.is_better_than(result2, ComparisonCriterion("precision", "max")))
        self.assertFalse(
            result1.is_better_than(result2, ComparisonCriterion("precision", "min")))
        self.assertFalse(result2.is_better_than(result1, ComparisonCriterion("precision", "max")))

        result3 = self.get_job_result({JobResult.STATUS: 1})
        result4 = self.get_job_result({})
        self.assertTrue(result3.is_better_than(result4))

    def test_can_compare_with_metric(self):
        result1 = self.get_job_result(precision_at_k=0.8)
        result2 = self.get_job_result(precision_at_k=0.3)
        self.assertTrue(result1._can_compare_with_metric(result2, SupportedTraceMetric.PRECISION.name))
        self.assertFalse(result1._can_compare_with_metric(result2, None))
        self.assertFalse(result1._can_compare_with_metric(result2, "precision_at_k"))

    def test_get_comparison_vals(self):
        result1 = self.get_job_result(precision_at_k=0.8)
        result2 = self.get_job_result(precision_at_k=0.3)
        metric1, metric2 = result1._get_comparison_vals(result2, SupportedTraceMetric.PRECISION.name)
        self.assertEquals(metric1, 0.8)
        self.assertEquals(metric2, 0.3)

        result1.set_job_status(Status.SUCCESS)
        val1, val2 = result1._get_comparison_vals(result2, "unknown")
        self.assertEquals(val1, Status.SUCCESS)
        self.assertEquals(val2, Status.UNKNOWN)

    def test_unknown_value(self):
        result = self.get_job_result()
        try:
            result["unknown"] = 2
            self.fail("Exception not raised for unknown value")
        except ValueError:
            pass

    def get_job_result(self, results_dict=None, precision_at_k=0.8):
        if results_dict is None:
            results_dict = {JobResult.BODY: {TracePredictionOutput.METRICS: {SupportedTraceMetric.PRECISION.name: precision_at_k}}}
        return JobResult(results_dict)
