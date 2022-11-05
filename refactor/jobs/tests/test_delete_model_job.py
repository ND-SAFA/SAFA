import os

from api.responses.base_response import BaseResponse
from jobs.delete_model_job import DeleteModelJob
from jobs.job_status import Status
from test.base_test import BaseTest
from test.config.paths import TEST_OUTPUT_DIR


class TestDeleteModelJob(BaseTest):
    DIR2DELETE = "dir2delete"
    MODEL_DIR = os.path.join(TEST_OUTPUT_DIR, DIR2DELETE)
    TEST_PARAMS = BaseTest.get_test_params()

    def test_run_dir_exists(self):
        self.make_test_output_dir()
        test_model_job = self.get_test_model_job()
        test_model_job.run()
        self.assertFalse(os.path.exists(self.MODEL_DIR))
        self.output_test_success(test_model_job.result)

    def test_run_dir_does_not_exist(self):
        test_model_job = self.get_test_model_job()
        test_model_job.run()
        self.output_test_success(test_model_job.result)

    def output_test_success(self, output_dict: dict):
        self.assertIn(BaseResponse.STATUS, output_dict)
        self.assertEquals(output_dict[BaseResponse.STATUS], Status.SUCCESS)

    def make_test_output_dir(self):
        if not os.path.exists(self.MODEL_DIR):
            os.makedirs(self.MODEL_DIR)
        with open(os.path.join(self.MODEL_DIR, "test.txt"), "w") as test_file:
            test_file.write("This is a test.")

    def get_test_model_job(self):
        return DeleteModelJob(model_path=self.MODEL_DIR, output_dir=TEST_OUTPUT_DIR)
