
from api.responses.base_response import BaseResponse
from jobs.create_model_job import CreateModelJob
from test.base_job_test import BaseJobTest


class TestCreateModelJob(BaseJobTest):
    TEST_PARAMS = BaseJobTest.get_test_params(include_pre_processing=False)

    def test_run_success(self):
        self._test_run_success()

    def test_run_failure(self):
        self._test_run_failure()

    def _get_job(self):
        return CreateModelJob(**self.TEST_PARAMS)

    def _assert_success(self, output_dict: dict):
        self.assertIn(BaseResponse.MODEL_PATH, output_dict)
        self.assertEqual(output_dict[BaseResponse.MODEL_PATH], self.TEST_PARAMS["output_dir"])
