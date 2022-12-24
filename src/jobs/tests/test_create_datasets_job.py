from data.datasets.dataset_role import DatasetRole
from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult
from jobs.create_datasets_job import CreateDatasetsJob
from jobs.tests.base_job_test import BaseJobTest


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
        test_params = self.get_job_args(dataset_role=DatasetRole.TRAIN, include_links=True)
        job_args = JobArgs(**test_params)
        if not include_dataset:
            job_args.trainer_args.trainer_dataset_container[DatasetRole.TRAIN] = None
        return CreateDatasetsJob(job_args)
