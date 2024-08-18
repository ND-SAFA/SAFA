from typing import List

from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.jobs.abstract_job import AbstractJob, JobResult
from gen_common.jobs.job_args import JobArgs
from gen_common.summarize.artifact.artifacts_summarizer import ArtifactsSummarizer
from gen_common.summarize.jobs.summarize_job import SummarizeJob
from gen_common.util.enum_util import EnumDict
from gen_common.util.file_util import FileUtil
from gen_common.util.prompt_util import PromptUtil
from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.responses.summary import PROJECT_SUMMARY_RESPONSES
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.tests.base_job_test import BaseJobTest
from gen_common_test.testprojects.generation_test_project import GenerationTestProject


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
            project_summary_components = PROJECT_SUMMARY_RESPONSES
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
