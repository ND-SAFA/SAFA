from api.tests.api_base_test import APIBaseTest
from api.tests.common.mock_async import mock_async
from api.tests.common.test_data_creator import TestDataCreator
from api.tests.common.test_verifier import TestVerifier
from tgen.common.constants.project_summary_constants import DEFAULT_PROJECT_SUMMARY_SECTIONS
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.jobs.summary_jobs.summary_response import SummaryResponse
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestProjectSummary(APIBaseTest):

    @mock_async
    def test_sync_summarize(self, test_manager: TestAIManager):
        """
        Verifies that project summary endpoint is able to summarize artifacts and create project summary.
        """
        n_artifacts = 6
        layer_id = "TypeScript"
        extension = ".ts"
        artifacts = TestDataCreator.create_artifacts(layer_id, n_artifacts=n_artifacts, extension=extension)

        section_body_map = {s: f"{s} body." for s in DEFAULT_PROJECT_SUMMARY_SECTIONS}
        section_bodies = list(section_body_map.values())

        test_manager.mock_summarization()
        test_manager.mock_project_summary(section_body_map)

        data = {"artifacts": artifacts}
        response: SummaryResponse = self.request("/project-summary/", data)
        response_artifacts = response["artifacts"]
        summary = response["summary"]

        TestVerifier.assert_all_in(summary, section_bodies)
        TestVerifier.verify_artifacts(artifacts, response_artifacts, ignore_keys=[ArtifactKeys.SUMMARY])
