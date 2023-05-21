from unittest import mock

from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.hgen_jobs.generate_artifacts_job import GenerateArtifactsJob
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.testres.test_open_ai_responses import fake_open_ai_completion
from tgen.testres.testprojects.generation_test_project import GenerationTestProject
from tgen.train.args.open_ai_args import OpenAIArgs


class TestSingleArtifactGenerationJob(BaseJobTest):
    project = GenerationTestProject()
    ARTIFACTS_BY_CLUSTER = [["s1", "s2"], ["s3"]]

    @mock.patch.object(OpenAIManager, "make_completion_request_impl", side_effect=fake_open_ai_completion)
    def test_run_success(self, fake_open_ai_completion_mock: mock.MagicMock):
        """
        Tests that job is completed successfully.
        """
        self._test_run_success()

    def _assert_success(self, job: AbstractJob, job_result: JobResult):
        artifact_content = [artifact[ArtifactKeys.CONTENT] for id_, artifact in job_result.body.artifact_df.itertuples()
                            if artifact[ArtifactKeys.LAYER_ID] != job.SOURCE_LAYER_ID]
        self.assertEqual(len(artifact_content), len(self.ARTIFACTS_BY_CLUSTER))
        for i, artifact_ids in enumerate(self.ARTIFACTS_BY_CLUSTER):
            for a_id in artifact_ids:
                expected_artifact = self.project.get_artifact(a_id)
                self.assertIn(expected_artifact[ArtifactKeys.CONTENT.value], artifact_content[i])

    def _get_job(self) -> AbstractJob:
        llm_manager = OpenAIManager(OpenAIArgs())
        return GenerateArtifactsJob(self.project.ARTIFACTS, "user_story", llm_manager, self.ARTIFACTS_BY_CLUSTER)
