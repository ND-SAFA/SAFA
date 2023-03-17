from unittest import skip

from jobs.abstract_job import AbstractJob
from jobs.components.job_result import JobResult
from jobs.create_datasets_job import CreateDatasetsJob
from jobs.export_dataset_job import ExportDatasetJob
from jobs.tests.base_job_test import BaseJobTest
from testres.paths.paths import TEST_OUTPUT_DIR
from util.object_creator import ObjectCreator
from variables.typed_definition_variable import TypedDefinitionVariable


class TestExportDatasetJob(BaseJobTest):
    """
    Tests ability to export dataset as SAFA.
    """
    job_definition = {
        "exporter": {
            TypedDefinitionVariable.OBJECT_TYPE_KEY: "SAFA",
            "dataset_creator": {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "TRACE",
                **ObjectCreator.dataset_creator_definition
            },
            "export_path": TEST_OUTPUT_DIR}
    }

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

    def _get_job(self, **kwargs) -> AbstractJob:
        """
        Constructs job for testing.
        """
        definition = {**self.job_definition, "job_args": {"output_dir": TEST_OUTPUT_DIR}}
        return ObjectCreator.create(ExportDatasetJob, override=True, **definition)
