from unittest import skip

from tgen.common.util.status import Status
from tgen.jobs.summary_jobs.project_summary_job import ProjectSummaryJob
from tgen.jobs.summary_jobs.summary_response import SummaryResponse
from tgen.prompts.supported_prompts.project_summary_prompts import PROJECT_SUMMARY_SECTIONS
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.mock_responses import MockResponses
from tgen.testres.mocking.test_response_manager import TestAIManager
from tgen.testres.test_data_manager import TestDataManager


class TestProjectSummaryJob(BaseTest):
    @mock_anthropic
    def test_smoke_test(self, ai_manager: TestAIManager):
        """
        Tests that projects are able to be summarized.
        """

        ai_manager.mock_summarization()
        ai_manager.set_responses(MockResponses.project_summary_responses)
        project_reader = TestDataManager.get_project_reader()
        artifact_df, _, _ = project_reader.read_project()
        job = ProjectSummaryJob(artifacts=[artifact for i, artifact in artifact_df.itertuples()])
        job.run()
        self.assertEqual(Status.SUCCESS, job.result.status)

        project_summary_response: SummaryResponse = job.result.body
        project_summary = project_summary_response["summary"]

        for r, section in zip(MockResponses.project_summary_responses, PROJECT_SUMMARY_SECTIONS):
            self.assertIn(r, project_summary)
            self.assertIn(f"# {section}", project_summary)

    @skip
    def test_artifacts_present(self):
        """
        Tests that artifacts are present in project summary prompt.
        """
        raise NotImplemented()
