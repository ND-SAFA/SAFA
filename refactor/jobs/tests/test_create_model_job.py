from jobs.create_model_job import CreateModelJob
from jobs.job_args import JobArgs
from jobs.responses.base_response import BaseResponse
from test.base_job_test import BaseJobTest


class TestCreateModelJob(BaseJobTest):
    TEST_PARAMS = BaseJobTest.get_test_params()

    def test_run_success(self):
        self._test_run_success()

    def test_run_failure(self):
        self._test_run_failure()

    def _get_job(self):
        job_args = JobArgs(**self.TEST_PARAMS)
        return CreateModelJob(job_args)

    def _assert_success(self, output_dict: dict):
        self.assertIn(BaseResponse.MODEL_PATH, output_dict)
        self.assertEqual(output_dict[BaseResponse.MODEL_PATH], self.TEST_PARAMS["output_dir"])
