from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.create_datasets_job import CreateDatasetsJob
from test.jobs.base_job_test import BaseJobTest
from test.testres.object_creator import ObjectCreator


class TestCreateDatasetsJob(BaseJobTest):
    """
    Verifying successful job when saving datasets.
    """

    def test_run_success(self):
        """
        Tests that job is completed succesfully.
        """
        self._test_run_success()

    def _assert_success(self, _: CreateDatasetsJob, job_result: JobResult):
        """
        Verifies that output contains dataset output path.
        """
        self.assertIn(JobResult.SAVED_DATASET_PATHS, job_result)
        self.assertGreater(len(job_result[JobResult.SAVED_DATASET_PATHS]), 0)

    def test_run_failure(self):
        """
        Tests that error is propagated from job.
        """
        job = self._get_job(include_dataset=False)
        job.run()
        self.assert_output_on_failure(self._load_job_output(job))

    def _get_job(self, include_dataset=True) -> AbstractJob:
        """
        Creates job.
        """
        job_args = ObjectCreator.create(JobArgs)
        if not include_dataset:
            trainer_dataset_manager = ObjectCreator.create(TrainerDatasetManager, **{}, override=True)

        else:
            trainer_dataset_manager = ObjectCreator.create(TrainerDatasetManager)

        return CreateDatasetsJob(job_args=job_args, export_path=job_args.output_dir,
                                 trainer_dataset_manager=trainer_dataset_manager)
