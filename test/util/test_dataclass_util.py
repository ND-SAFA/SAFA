import uuid

from tgen.common.util.dataclass_util import DataclassUtil
from tgen.common.util.status import Status
from tgen.jobs.components.job_result import JobResult
from tgen.testres.base_tests.base_test import BaseTest


class TestDataclasssUtil(BaseTest):

    def test_convert_to_dict(self):
        job_id = uuid.uuid4()
        job_result = JobResult(job_id=job_id, status=Status.UNKNOWN)

        dict_ = DataclassUtil.convert_to_dict(job_result)
        self.assertEqual(dict_["job_id"], job_id)
        self.assertEqual(dict_["status"], Status.UNKNOWN)

        dict_ = DataclassUtil.convert_to_dict(job_result, status=Status.SUCCESS)
        self.assertEqual(dict_["job_id"], job_id)
        self.assertEqual(dict_["status"], Status.SUCCESS)