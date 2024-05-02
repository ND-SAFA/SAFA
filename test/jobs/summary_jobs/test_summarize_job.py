from typing import List

from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.summary_jobs.summarize_job import SummarizeJob
from tgen.summarizer.artifact.artifacts_summarizer import ArtifactsSummarizer
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.mock_responses import MockResponses
from tgen.testres.mocking.test_response_manager import TestAIManager
from tgen.testres.testprojects.generation_test_project import GenerationTestProject


class TestSummarizeJob(BaseJobTest):
    CODE_SUMMARY = "CODE SUMMARY"
    NL_SUMMARY = "NL SUMMARY"
    RESUMMARIZED = "resummarized"
    N_ARTIFACTS = 4

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
        responses = self.get_summarize_responses()[:self.N_ARTIFACTS]

        ai_manager.set_responses(responses)
        job_args = JobArgs(dataset=self.get_project().get_dataset())
        job = SummarizeJob(job_args,
                           is_subset=True, summarize_code_only=False, do_resummarize_artifacts=True)
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
        if not resummarize:
            project_summary_components = MockResponses.project_summary_responses
            responses.extend(project_summary_components)
        return responses

    def _assert_success(self, job: AbstractJob, job_result: JobResult, resummarized: bool = True):
        artifacts = job_result.body["artifacts"]
        for artifact in artifacts:
            artifact = EnumDict(artifact)
            artifact_id = artifact[ArtifactKeys.ID]
            expected_artifact = self.get_project().get_artifact(artifact_id)
            if resummarized:
                self.assertIn(self.RESUMMARIZED, artifact[ArtifactKeys.SUMMARY])
            else:
                self.assertNotIn(self.RESUMMARIZED, artifact[ArtifactKeys.SUMMARY])
            if FileUtil.is_code(expected_artifact[ArtifactKeys.ID.value]):
                self.assertIn(self.CODE_SUMMARY, artifact[ArtifactKeys.SUMMARY])
            else:
                self.assertIn(self.NL_SUMMARY, artifact[ArtifactKeys.SUMMARY])

    def _get_job(self) -> AbstractJob:
        return SummarizeJob(JobArgs(dataset=self.get_project().get_dataset()),
                            summarize_code_only=False, do_resummarize_artifacts=True)

    def get_project(self):
        return GenerationTestProject()
