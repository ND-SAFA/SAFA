from unittest import mock

from tgen.common.util.enum_util import EnumDict
from tgen.data.chunkers.java_chunker import JavaChunker
from tgen.data.chunkers.python_chunker import PythonChunker
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.summarizer.summarizer import Summarizer
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.data_jobs.summarize_artifacts_job import SummarizeArtifactsJob
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.testres.testprojects.generation_test_project import GenerationTestProject
from tgen.testres.testprojects.mocking.mock_anthropic import mock_anthropic
from tgen.testres.testprojects.mocking.test_response_manager import TestAIManager


class TestSummarizeJob(BaseJobTest):
    project = GenerationTestProject()
    ARTIFACT_MAP = {f"s{i + 1}": i for i in range(len(project.ARTIFACTS))}

    @mock.patch.object(PythonChunker, "chunk", side_effect=lambda content, **kwargs: ["python " + content])
    @mock.patch.object(JavaChunker, "chunk", side_effect=lambda content, **kwargs: ["java " + content])
    @mock_anthropic
    def test_run_success(self, ai_manager: TestAIManager, fake_java_chunk: mock.MagicMock, fake_python_chunk: mock.MagicMock):
        """
        Tests that job is completed succesfully.
        """
        ai_manager.mock_summarization()
        self._test_run_success()

    def _assert_success(self, job: AbstractJob, job_result: JobResult):
        for artifact_id, artifact in job_result.body.items():
            artifact = EnumDict(artifact)
            expected_artifact = self.project.get_artifact(artifact_id)
            self.assertIn("Summary of", artifact[ArtifactKeys.SUMMARY])
            if expected_artifact[SummarizeArtifactsJob.TYPE_KEY] == "py":
                self.assertIn("python", artifact[ArtifactKeys.SUMMARY])
            elif expected_artifact[SummarizeArtifactsJob.TYPE_KEY] == "java":
                self.assertIn("java", artifact[ArtifactKeys.SUMMARY])
            else:
                self.assertNotIn("python", artifact[ArtifactKeys.SUMMARY])
                self.assertNotIn("java", artifact[ArtifactKeys.SUMMARY])

    def _get_job(self) -> AbstractJob:
        return SummarizeArtifactsJob(self.project.ARTIFACTS, summarizer=Summarizer(AnthropicManager()))
