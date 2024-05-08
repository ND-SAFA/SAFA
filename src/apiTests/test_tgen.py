from apiTests.base_test import BaseTest
from apiTests.common.request_proxy import RequestProxy
from apiTests.common.test_data import TestData, TestSubset
from apiTests.common.test_verifier import TestVerifier
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestTGen(BaseTest):

    @mock_anthropic
    def test_use_case(self, ai_manager: TestAIManager) -> None:
        """
        Traces between the source and target artifacts of test dataset.
        :param ai_manager: The AI manages used to mock responses.
        :return: None
        """
        for sync in [True, False]:
            dataset = TestData.get_dataset(TestSubset.FULL)

            if not sync:
                ai_manager.mock_ranking(artifact_ids=[0, 1, 2, 3], scores=[5, 5, 2, 2])
                ai_manager.mock_ranking(artifact_ids=[0, 1, 2, 3], scores=[5, 5, 2, 2])
                ai_manager.mock_explanations(8)

            trace_predictions = RequestProxy.trace(dataset, sync=sync)
            self.assertEqual(8, len(trace_predictions))
            TestVerifier.verify_order(self, {
                "FR1": ["/Artifact.java", "/ArtifactService.java", "/TraceLink.java", "/TraceLinkService.java"],
                "FR2": ["/TraceLink.java", "/TraceLinkService.java", "/Artifact.java", "/ArtifactService.java", "A"]
            }, trace_predictions, msg_suffix=f"\n while sync={sync}")
