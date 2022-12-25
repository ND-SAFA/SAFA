import os

from jobs.components.job_args import JobArgs
from jobs.delete_model_job import DeleteModelJob
from jobs.tests.base_job_test import BaseJobTest
from models.model_manager import ModelManager
from test.paths.paths import TEST_OUTPUT_DIR
from test.test_object_creator import TestObjectCreator


class TestDeleteModelJob(BaseJobTest):
    DIR2DELETE = "dir2delete"
    MODEL_DIR = os.path.join(TEST_OUTPUT_DIR, DIR2DELETE)

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
        job_args = JobArgs(output_dir=TEST_OUTPUT_DIR)
        model_manager = TestObjectCreator.create(ModelManager, **{
            "model_path": self.MODEL_DIR
        })
        return DeleteModelJob(job_args=job_args, model_manager=model_manager)
