from typing import List

from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.summarizer.artifacts_summarizer import ArtifactsSummarizer
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.summary_jobs.summarize_artifacts_job import SummarizeArtifactsJob
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.testres.testprojects.generation_test_project import GenerationTestProject
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestSummarizeJob(BaseJobTest):
    project = GenerationTestProject()
    CODE_SUMMARY = "CODE SUMMARY"
    NL_SUMMARY = "NL SUMMARY"
    RESUMMARIZED = "resummarized"
    PROJECT_SUMMARY = "project summary"

    @mock_anthropic
    def test_run_success(self, ai_manager: TestAIManager):
        """
        Tests that job is completed succesfully.
        """
        responses = self.get_summarize_responses() + self.get_summarize_responses(resummarize=True)

        ai_manager.set_responses(responses)

        self._test_run_success()

    @mock_anthropic
    def test_run_subset_of_artifacts(self, ai_manager: TestAIManager):
        responses = self.get_summarize_responses()[:-1]

        ai_manager.set_responses(responses)
        job = SummarizeArtifactsJob(self.project.ARTIFACTS, is_subset=True)
        job.run()
        self.assert_output_on_success(job, job.result, resummarized=False)

    def get_summarize_responses(self, resummarize: bool = False) -> List:
        responses = []
        for artifact in GenerationTestProject.ARTIFACTS:
            if FileUtil.is_code(artifact[ArtifactKeys.ID.value]):
                summary = self.CODE_SUMMARY
            else:
                summary = self.NL_SUMMARY
            if resummarize:
                summary = f"{self.RESUMMARIZED} {summary}"
            responses.append(PromptUtil.create_xml(ArtifactsSummarizer.SUMMARY_TAG, summary))
        project_summary = self.PROJECT_SUMMARY
        if resummarize:
            project_summary = f"{self.RESUMMARIZED} {project_summary}"
        responses.append(project_summary)
        return responses

    def _assert_success(self, job: AbstractJob, job_result: JobResult, resummarized: bool = True):
        artifacts = job_result.body["artifacts"]
        for artifact_id, artifact in artifacts.items():
            artifact = EnumDict(artifact)
            expected_artifact = self.project.get_artifact(artifact_id)
            if resummarized:
                self.assertIn(self.RESUMMARIZED, artifact[ArtifactKeys.SUMMARY])
            else:
                self.assertNotIn(self.RESUMMARIZED, artifact[ArtifactKeys.SUMMARY])
            if FileUtil.is_code(expected_artifact[ArtifactKeys.ID.value]):
                self.assertIn(self.CODE_SUMMARY, artifact[ArtifactKeys.SUMMARY])
            else:
                self.assertIn(self.NL_SUMMARY, artifact[ArtifactKeys.SUMMARY])
        if resummarized:
            self.assertEqual(f"{self.RESUMMARIZED} {self.PROJECT_SUMMARY}", job_result.body["summary"])

    def _get_job(self) -> AbstractJob:
        return SummarizeArtifactsJob(self.project.ARTIFACTS)
