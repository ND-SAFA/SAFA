from test.concepts.constants import ConceptData
from test.concepts.utils import create_concept_args
from tgen.concepts.concept_state import ConceptState
from tgen.concepts.steps.entity_matching_step import EntityMatching
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestEntityMatching(BaseTest):
    N_MATCHES = 2

    @mock_anthropic
    def test_entity_matching(self, ai_manager: TestAIManager):
        """
        Tests that entities predicted
        :param ai_manager:
        :return:
        """
        args = create_concept_args()
        state = ConceptState()
        state.entity_df = ConceptData.get_entity_df()

        self.mock_entity_matching(ai_manager)
        step = EntityMatching()
        step.run(args, state)

        predicted_links = state.predicted_matches
        self.assertEqual(TestEntityMatching.N_MATCHES, len(predicted_links))
        for i in range(TestEntityMatching.N_MATCHES):
            link = predicted_links[i]
            self.assertEqual(ConceptData.Predicted[i]["source"], link["source"])
            self.assertEqual(ConceptData.Predicted[i]["target"], link["target"])

    @staticmethod
    def mock_entity_matching(ai_manager: TestAIManager) -> None:
        """
        Mocks response for entity matching.
        :param ai_manager: AI manager to add responses to.
        :return:None.
        """
        ai_manager.add_responses([
            EntityMatching.create_example_xml(ConceptData.Predicted[0]["target"]),
            EntityMatching.create_example_xml(ConceptData.Predicted[1]["target"]),
            "NA"
        ])
