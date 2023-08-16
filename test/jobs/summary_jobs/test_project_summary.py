from unittest import skip

from tgen.jobs.summary_jobs.project_summary_job import ProjectSummaryJob, ProjectSummaryResponse
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.test_data_manager import TestDataManager
from tgen.testres.testprojects.mocking.mock_anthropic import mock_anthropic
from tgen.testres.testprojects.mocking.test_response_manager import TestAIManager


class TestProjectSummaryJob(BaseTest):
    @mock_anthropic
    def test_smoke_test(self, ai_manager: TestAIManager):
        """
        Tests that projects are able to be summarized.
        """
        project_summary = "project_summary"
        ai_manager.set_responses([project_summary])
        project_reader = TestDataManager.get_project_reader()
        artifact_df, _, _ = project_reader.read_project()
        job = ProjectSummaryJob(artifact_map=artifact_df.to_map())
        job.run()
        project_summary_response: ProjectSummaryResponse = job.result.body
        self.assertEqual(project_summary, project_summary_response["summary"])

    @skip
    def test_artifacts_present(self):
        """
        Tests that artifacts are present in project summary prompt.
        """
        raise NotImplemented()
