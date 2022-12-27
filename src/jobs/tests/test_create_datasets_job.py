from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult
from jobs.create_datasets_job import CreateDatasetsJob
from jobs.tests.base_job_test import BaseJobTest
from test.test_object_creator import TestObjectCreator


class TestCreateDatasetsJob(BaseJobTest):

    def test_run_success(self):
        self._test_run_success()

    def _assert_success(self, output_dict: dict):
        self.assertIn(JobResult.SAVED_DATASET_PATHS, output_dict)
        self.assertGreater(len(output_dict[JobResult.SAVED_DATASET_PATHS]), 0)

    def test_run_failure(self):
        job = self._get_job(include_dataset=False)
        job.run()
        self.assert_output_on_failure(self._load_job_output(job))

    def _get_job(self, include_dataset=True) -> AbstractJob:
        job_args = TestObjectCreator.create(JobArgs)
        if not include_dataset:
            trainer_dataset_manager = TestObjectCreator.create(TrainerDatasetManager, **{}, override=True)

        else:
            trainer_dataset_manager = TestObjectCreator.create(TrainerDatasetManager)

        return CreateDatasetsJob(job_args=job_args, trainer_dataset_manager=trainer_dataset_manager)
