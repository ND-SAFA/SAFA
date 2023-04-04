from unittest import skip

from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.exporters.supported_dataset_exporters import SupportedDatasetExporter
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.create_datasets_job import CreateDatasetsJob
from test.jobs.base_job_test import BaseJobTest
from test.testres.paths.paths import TEST_OUTPUT_DIR
from test.testres.object_creator import ObjectCreator


class TestCreateDatasetJobSAFA(BaseJobTest):
    """
    Tests ability to export dataset as SAFA.
    """

    def test_run_success(self):
        """
        Tests that run completes successfully.
        """
        self._test_run_success()

    def _assert_success(self, _: CreateDatasetsJob, job_result: JobResult):
        """
        Tests that output contains dataset output path.
        """
        self.assertIn(JobResult.SAVED_DATASET_PATHS, job_result)
        self.assertGreater(len(job_result[JobResult.SAVED_DATASET_PATHS]), 0)

    def _get_job(self, include_dataset=True) -> AbstractJob:
        """
        Creates job.
        """
        job_args = ObjectCreator.create(JobArgs)
        dataset_creator = ObjectCreator.create(TraceDatasetCreator)
        trainer_dataset_manager = TrainerDatasetManager(train_dataset_creator=dataset_creator)
        return CreateDatasetsJob(job_args=job_args, export_path=TEST_OUTPUT_DIR, trainer_dataset_manager=trainer_dataset_manager,
                                 format_type=SupportedDatasetExporter.SAFA)
