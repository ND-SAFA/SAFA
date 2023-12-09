from tests.base_test import BaseTest
from tests.common.request_proxy import RequestProxy
from tests.common.test_data import TestData, TestSubset
from tests.common.test_verifier import TestVerifier
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestTGen(BaseTest):

    @mock_anthropic
    def test_use_case(self, ai_manager: TestAIManager):
        """
        Traces between the source and target artifacts of test dataset.
        """
        for sync in [True, False]:
            dataset = TestData.get_dataset(TestSubset.FULL)

            if not sync:
                ai_manager.mock_ranking(artifact_ids=[0, 1, 2, 3], scores=[5, 4, 2, 1])
                ai_manager.mock_ranking(artifact_ids=[0, 1, 2, 3], scores=[1, 2, 4, 5])
                ai_manager.mock_explanations(artifacts=[0, 1, 2, 3])
                ai_manager.mock_explanations(artifacts=[0, 1, 2, 3])

            trace_predictions = RequestProxy.trace(dataset, sync=sync)
            self.assertEqual(8, len(trace_predictions))
            TestVerifier.verify_order(self, trace_predictions, {
                "FR1": ["/Artifact.java", "/ArtifactService.java", "/TraceLink.java", "/TraceLinkService.java"],
                "FR2": ["/TraceLink.java", "/TraceLinkService.java", "/Artifact.java", "/ArtifactService.java"]
            })
