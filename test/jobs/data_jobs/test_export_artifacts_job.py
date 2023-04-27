from tgen.constants.deliminator_constants import NEW_LINE
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.data_jobs.create_datasets_job import CreateDatasetsJob
from tgen.jobs.data_jobs.export_artifacts_job import ExportArtifactsJob
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.testres.test_data_manager import TestDataManager
from tgen.util.file_util import FileUtil
from tgen.testres.object_creator import ObjectCreator


class TestExportArtifactsJob(BaseJobTest):
    """
    Tests that you can export a project's artifacts as a delimited file.
    """

    def test_run_success(self):
        """
        Test that exported file contains every artifact body.
        """
        self._test_run_success()

    def _assert_success(self, _: CreateDatasetsJob, job_result: JobResult):
        """
        Verifies that file containing same number of lines as artifacts and each artifact is
        present in exported file.
        """
        export_path = job_result[JobResult.EXPORT_PATH]
        self.assertIsNotNone(export_path)
        file_lines = FileUtil.read_file(export_path).split(NEW_LINE)
        artifacts = TestDataManager.get_artifact_map()
        self.assertEqual(len(artifacts), len(file_lines))
        for _, a_body in artifacts.items():
            self.assertIn(a_body, file_lines)

    def test_run_failure(self):
        """
        Verifies that null delimiter causes exception returned by job result.
        """
        job = self._get_job(delimiter=None)
        job.run()
        self.assert_output_on_failure(self._load_job_output(job))

    def _get_job(self, **kwargs) -> ExportArtifactsJob:
        """
        Creates job to export project artifacts.
        """
        job_args = ObjectCreator.create(JobArgs)
        trainer_dataset_manager = ObjectCreator.create(TrainerDatasetManager)
        trace_project_creator: TraceDatasetCreator = trainer_dataset_manager.get_creator(DatasetRole.TRAIN)
        return ExportArtifactsJob(trace_project_creator, job_args, **kwargs)
