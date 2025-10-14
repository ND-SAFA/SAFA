from apiTests.base_test import BaseTest
from apiTests.common.request_proxy import RequestProxy
from apiTests.common.test_data_creator import TestDataCreator
from apiTests.common.test_verifier import TestVerifier
from gen.summary.summary_response import SummaryResponse
from gen_common.constants.summary_constants import DEFAULT_PROJECT_SUMMARY_SECTIONS
from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager


class TestProjectSummary(BaseTest):

    @mock_anthropic
    def test_use_case(self, test_manager: TestAIManager):
        """
        Verifies that project summary endpoint is able to summarize artifacts and create project summary.
        """
        artifacts = TestDataCreator.get_source_artifacts()

        section_body_map = {s: f"{s} body." for s in DEFAULT_PROJECT_SUMMARY_SECTIONS}

        test_manager.mock_summarization()
        test_manager.mock_project_summary(section_body_map)

        response: SummaryResponse = RequestProxy.summarize(artifacts)
        response_artifacts = response["artifacts"]
        summary = response["summary"]

        section_bodies = list(section_body_map.values())
        TestVerifier.assert_all_in(self, summary, section_bodies)
        TestVerifier.verify_artifacts(self, artifacts, response_artifacts, ignore_keys=[ArtifactKeys.SUMMARY, ArtifactKeys.CHUNKS])
