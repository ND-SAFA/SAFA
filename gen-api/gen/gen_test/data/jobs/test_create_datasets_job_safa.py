from gen_common.data.creators.trace_dataset_creator import TraceDatasetCreator
from gen_common.data.exporters.supported_dataset_exporters import SupportedDatasetExporter
from gen_common.data.managers.trainer_dataset_manager import TrainerDatasetManager
from gen_common.infra.experiment.object_creator import ObjectCreator
from gen_common.jobs.abstract_job import AbstractJob, JobResult
from gen_common.jobs.job_args import JobArgs
from gen_common_test.base.tests.base_job_test import BaseJobTest

from gen.data.jobs.create_datasets_job import CreateDatasetsJob
from gen_test.res.paths import TEST_OUTPUT_DIR


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
        self.assertGreater(len(job_result.body), 0)

    def _get_job(self, include_dataset=True) -> AbstractJob:
        """
        Creates job.
        """
        job_args = ObjectCreator.create(JobArgs)
        dataset_creator = ObjectCreator.create(TraceDatasetCreator)
        trainer_dataset_manager = TrainerDatasetManager(train_dataset_creator=dataset_creator)
        job_args.export_dir = TEST_OUTPUT_DIR
        return CreateDatasetsJob(trainer_dataset_manager=trainer_dataset_manager, job_args=job_args,
                                 format_type=SupportedDatasetExporter.SAFA)
