import os

from jobs.delete_model_job import DeleteModelJob
from test.base_job_test import BaseJobTest
from test.config.paths import TEST_OUTPUT_DIR


class TestDeleteModelJob(BaseJobTest):
    DIR2DELETE = "dir2delete"
    MODEL_DIR = os.path.join(TEST_OUTPUT_DIR, DIR2DELETE)
    TEST_PARAMS = BaseJobTest.get_test_params()

    def test_run_success(self):
        self._test_run_success()

    def test_run_dir_exists(self):
        self.make_test_output_dir()
        job = self.get_job()
        job.run()
        output_dict = self._load_job_output(job)
        self.assert_output_on_success(output_dict)

    def make_test_output_dir(self):
        if not os.path.exists(self.MODEL_DIR):
            os.makedirs(self.MODEL_DIR)
        with open(os.path.join(self.MODEL_DIR, "test.txt"), "w") as test_file:
            test_file.write("This is a test.")

    def _assert_success(self, output_dict: dict):
        self.assertFalse(os.path.exists(self.MODEL_DIR))

    def _get_job(self):
        return DeleteModelJob(model_path=self.MODEL_DIR, output_dir=TEST_OUTPUT_DIR)
