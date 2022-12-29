from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult
from jobs.create_model_job import CreateModelJob
from jobs.tests.base_job_test import BaseJobTest
from models.model_manager import ModelManager
from test.paths.paths import TEST_OUTPUT_DIR
from util.object_creator import TestObjectCreator


class TestCreateModelJob(BaseJobTest):

    def test_run_success(self):
        self._test_run_success()

    def test_run_failure(self):
        self._test_run_failure()

    def _get_job(self):
        job_args = TestObjectCreator.create(JobArgs)
        model_manager: ModelManager = TestObjectCreator.create(ModelManager)
        return CreateModelJob(job_args=job_args, model_manager=model_manager)

    def _assert_success(self, output_dict: dict):
        self.assertIn(JobResult.MODEL_PATH, output_dict)
        self.assertEqual(output_dict[JobResult.MODEL_PATH], TEST_OUTPUT_DIR)
