from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.model_jobs.create_model_job import CreateModelJob
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.models.model_manager import ModelManager
from tgen.testres.paths.paths import TEST_OUTPUT_DIR
from tgen.testres.object_creator import ObjectCreator


class TestCreateModelJob(BaseJobTest):

    def test_run_success(self):
        self._test_run_success()

    def test_run_failure(self):
        self._test_run_failure()

    def _get_job(self):
        job_args = ObjectCreator.create(JobArgs)
        model_manager: ModelManager = ObjectCreator.create(ModelManager)
        return CreateModelJob(job_args=job_args, model_manager=model_manager)

    def _assert_success(self, job: CreateModelJob, output_dict: dict):
        self.assertEqual(output_dict.body, TEST_OUTPUT_DIR)
