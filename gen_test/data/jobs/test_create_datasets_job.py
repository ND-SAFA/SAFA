from gen_common.data.managers.trainer_dataset_manager import TrainerDatasetManager
from gen_common.infra.experiment.object_creator import ObjectCreator
from gen_common.jobs.abstract_job import AbstractJob, JobResult
from gen_common.jobs.job_args import JobArgs
from gen_common_test.base.tests.base_job_test import BaseJobTest

from gen.data.jobs.create_datasets_job import CreateDatasetsJob


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
        self.assertGreater(len(job_result.body), 0)

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
        job_args.export_dir = job_args.output_dir
        return CreateDatasetsJob(trainer_dataset_manager=trainer_dataset_manager, job_args=job_args)
