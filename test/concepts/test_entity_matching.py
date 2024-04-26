from test.concepts.constants import CONCEPT_ARTIFACT_ID, CONCEPT_ENTITY_MATCHED
from test.concepts.utils import create_concept_args, create_concept_test_entities
from tgen.concepts.concept_state import ConceptState
from tgen.concepts.steps.entity_matching import EntityMatching
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_openai import mock_openai
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestEntityMatching(BaseTest):
    N_MATCHES = 1

    @mock_openai
    def test_entity_matching(self, ai_manager: TestAIManager):
        args = create_concept_args()
        state = ConceptState()
        state.entity_df = create_concept_test_entities()

        self.mock_entity_matching(ai_manager)
        step = EntityMatching()
        step.run(args, state)

        predicted_links = state.predicted_matches
        self.assertEqual(TestEntityMatching.N_MATCHES, len(predicted_links))
        self.assertEqual(CONCEPT_ARTIFACT_ID, predicted_links[0]["source"])
        self.assertEqual(CONCEPT_ENTITY_MATCHED, predicted_links[0]["target"])

    @staticmethod
    def mock_entity_matching(ai_manager: TestAIManager) -> None:
        """
        Mocks response for entity matching.
        :param ai_manager: AI manager to add responses to.
        :return:None.
        """
        ai_manager.add_responses([
            EntityMatching.create_example_xml(CONCEPT_ARTIFACT_ID, CONCEPT_ENTITY_MATCHED)
        ])
