from apiTests.base_test import BaseTest
from apiTests.common.request_proxy import RequestProxy
from apiTests.common.test_data import TestData, TestSubset
from apiTests.common.test_verifier import TestVerifier
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestTGen(BaseTest):
    """
    Traces between the source and target artifacts of test dataset.
    """

    def test_use_case_sync(self) -> None:
        """
        Performs traceability using just an embedding model to rank the candidate artifacts.
        """
        self.run_tgen_case()

    @mock_anthropic
    def test_use_case(self, ai_manager: TestAIManager) -> None:
        """
        Performs traceability by refining the rankings of the embedding model using an LLM.
        """
        self.run_tgen_case(ai_manager)

    def run_tgen_case(self, ai_manager=None) -> None:
        """
        Performs a ranking job against test dataset, creates mock responses if an AI manager is given.
        :param ai_manager: Optional AI manager to use to mock ranking responses.
        :return: None
        """
        dataset = TestData.get_dataset(TestSubset.FULL)

        if ai_manager:
            ai_manager.mock_ranking(artifact_ids=[0, 1, 2, 3], scores=[5, 5, 2, 2])
            ai_manager.mock_ranking(artifact_ids=[0, 1, 2, 3], scores=[5, 5, 2, 2])
            ai_manager.mock_explanations(8)

        is_sync = ai_manager is None
        trace_predictions = RequestProxy.trace(dataset, sync=is_sync)
        self.assertEqual(8, len(trace_predictions))
        TestVerifier.verify_order(self, {
            "FR1": ["/Artifact.java", "/ArtifactService.java", "/TraceLink.java", "/TraceLinkService.java"],
            "FR2": ["/TraceLink.java", "/TraceLinkService.java", "/Artifact.java", "/ArtifactService.java"]
        }, trace_predictions, msg_suffix=f"\n while sync={is_sync}")
