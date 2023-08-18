from unittest import mock

from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.chunkers.java_chunker import JavaChunker
from tgen.data.chunkers.python_chunker import PythonChunker
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.summarizer.summarizer import Summarizer
from tgen.data.summarizer.summary_types import SummaryTypes
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
    CODE_SUMMARY = "CODE SUMMARY"
    NL_SUMMARY = "NL SUMMARY"

    @mock_anthropic
    def test_run_success(self, ai_manager: TestAIManager):
        """
        Tests that job is completed succesfully.
        """
        responses = []
        for artifact in GenerationTestProject.ARTIFACTS:
            if FileUtil.is_code(artifact[ArtifactKeys.ID.value]):
                responses.append(PromptUtil.create_xml(Summarizer.SUMMARY_TAG, self.CODE_SUMMARY))
            else:
                responses.append(PromptUtil.create_xml(Summarizer.SUMMARY_TAG, self.NL_SUMMARY))
        ai_manager.set_responses(responses)
        self._test_run_success()

    def _assert_success(self, job: AbstractJob, job_result: JobResult):
        for artifact_id, artifact in job_result.body.items():
            artifact = EnumDict(artifact)
            expected_artifact = self.project.get_artifact(artifact_id)
            if FileUtil.is_code(expected_artifact[ArtifactKeys.ID.value]):
                self.assertIn(self.CODE_SUMMARY, artifact[ArtifactKeys.SUMMARY])
            else:
                self.assertIn(self.NL_SUMMARY, artifact[ArtifactKeys.SUMMARY])

    def _get_job(self) -> AbstractJob:
        return SummarizeArtifactsJob(self.project.ARTIFACTS, summarizer=Summarizer(AnthropicManager()))
