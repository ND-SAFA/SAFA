import json
import uuid

from tgen.common.util.status import Status
from tgen.jobs.components.job_result import JobResult
from tgen.testres.base_tests.base_test import BaseTest


class TestJobResult(BaseTest):

    def test_set_get_job_status(self):
        result = self.get_job_result()
        self.assertEqual(result.status, Status.UNKNOWN)
        result.status = Status.SUCCESS
        self.assertEqual(result.status, Status.SUCCESS)

    def test_to_json_and_from_dict(self):
        result1 = self.get_job_result()
        json_result = result1.to_json()
        result2 = JobResult.from_dict(json.loads(json_result))
        self.assertEqual(result1, result2)

    def test_as_dict_and_from_dict(self):
        result1 = self.get_job_result()
        result_dict = result1.as_dict()
        result2 = JobResult.from_dict(result_dict)
        self.assertEqual(result1, result2)

    def get_job_result(self, **params):
        return JobResult(job_id=uuid.uuid4(), **params)
