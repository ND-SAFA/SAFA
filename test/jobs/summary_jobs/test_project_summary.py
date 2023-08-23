from unittest import skip

from tgen.common.util.enum_util import EnumDict
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.jobs.summary_jobs.project_summary_job import ProjectSummaryJob
from tgen.jobs.summary_jobs.summary_response import SummaryResponse
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.test_data_manager import TestDataManager
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestProjectSummaryJob(BaseTest):
    @mock_anthropic
    def test_smoke_test(self, ai_manager: TestAIManager):
        """
        Tests that projects are able to be summarized.
        """
        project_summary = "project_summary"
        ai_manager.mock_summarization()
        ai_manager.set_responses([project_summary])
        project_reader = TestDataManager.get_project_reader()
        artifact_df, _, _ = project_reader.read_project()
        job = ProjectSummaryJob(artifacts=[artifact for i, artifact in artifact_df.itertuples()])
        job.run()
        project_summary_response: SummaryResponse = job.result.body
        self.assertEqual(project_summary, project_summary_response["summary"])

    @skip
    def test_artifacts_present(self):
        """
        Tests that artifacts are present in project summary prompt.
        """
        raise NotImplemented()
