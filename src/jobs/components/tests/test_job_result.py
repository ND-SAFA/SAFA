import json

from jobs.components.job_result import JobResult
from jobs.components.job_status import JobStatus
from test.base_test import BaseTest
from train.metrics.supported_trace_metric import SupportedTraceMetric


class TestJobResult(BaseTest):

    def test_set_get_job_status(self):
        result = self.get_job_result()
        self.assertEquals(result.get_job_status(), JobStatus.UNKNOWN)
        result.set_job_status(JobStatus.SUCCESS)
        self.assertEquals(result.get_job_status(), JobStatus.SUCCESS)

    def test_update(self):
        result1 = self.get_job_result()
        result2 = self.get_job_result({JobResult.STATUS: 1})
        result1.update(result2)
        result1.update({JobResult.PREDICTIONS: [{"source": "s1", "target": "t2", "score": 0.9}]})
        self.assertIn(JobResult.METRICS.upper(), result1)
        self.assertIn(SupportedTraceMetric.PRECISION.name.lower(), result1[JobResult.METRICS])
        self.assertIn(JobResult.STATUS, result1)
        self.assertEquals(result1[JobResult.STATUS], 1)
        self.assertIn(JobResult.PREDICTIONS, result1)

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

    def test_get_properties(self):
        response_keys = [JobResult.MODEL_PATH, JobResult.STATUS, "doesnt exist"]
        properties = JobResult.get_properties(response_keys)
        self.assertIn(JobResult.MODEL_PATH, properties)
        self.assertIn(JobResult.STATUS, properties)
        self.assertEquals(properties[JobResult.STATUS].type, "integer")
        self.assertEquals(properties[JobResult.MODEL_PATH].type, "string")
        self.assertNotIn("doesnt exist", properties)

        properties = JobResult.get_properties(JobResult.STATUS)
        self.assertIn(JobResult.STATUS, properties)

    def test_is_better_than(self):
        result1 = self.get_job_result(precision_at_k=0.8)
        result2 = self.get_job_result(precision_at_k=0.3)
        self.assertTrue(
            result1.is_better_than(result2, SupportedTraceMetric.PRECISION, should_maximize=True))
        self.assertFalse(
            result1.is_better_than(result2, SupportedTraceMetric.PRECISION, should_maximize=False))
        self.assertFalse(result2.is_better_than(result1, SupportedTraceMetric.PRECISION, should_maximize=True))

        result3 = self.get_job_result({JobResult.STATUS: 1})
        result4 = self.get_job_result({})
        self.assertTrue(result3.is_better_than(result4, should_maximize=True))

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

        result1.set_job_status(JobStatus.SUCCESS)
        val1, val2 = result1._get_comparison_vals(result2, "unknown")
        self.assertEquals(val1, JobStatus.SUCCESS)
        self.assertEquals(val2, JobStatus.UNKNOWN)

    def test_unknown_value(self):
        result = self.get_job_result()
        try:
            result["unknown"] = 2
            self.fail("Exception not raised for unknown value")
        except ValueError:
            pass

    def get_job_result(self, results_dict=None, precision_at_k=0.8):
        if results_dict is None:
            results_dict = {JobResult.METRICS: {SupportedTraceMetric.PRECISION.name: precision_at_k}}
        return JobResult(results_dict)
