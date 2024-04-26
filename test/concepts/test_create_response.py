from test.concepts.constants import CONCEPT_ENTITY_UNDEFINED
from test.concepts.test_direct_concept_matches import TestDirectConceptMatches
from test.concepts.test_entity_matching import TestEntityMatching
from test.concepts.utils import create_concept_args, create_concept_test_entities
from tgen.concepts.concept_state import ConceptState
from tgen.concepts.steps.create_response import CreateResponse
from tgen.concepts.steps.direct_concept_matches import DirectConceptMatches
from tgen.concepts.steps.entity_matching import EntityMatching
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_openai import mock_openai
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestCreateResponse(BaseTest):
    @mock_openai
    def test_create_response(self, ai_manager: TestAIManager) -> None:
        """
        Tests the ability to create the final response for concept pipeline.
        :param ai_manager: AI manager used to mock entity matching.
        :return: None
        """
        args = create_concept_args()
        state = ConceptState()

        # Mock pipeline execution assumptions
        DirectConceptMatches().run(args, state)
        state.entity_df = create_concept_test_entities()
        TestEntityMatching.mock_entity_matching(ai_manager)
        EntityMatching().run(args, state)
        CreateResponse().run(args, state)

        res = state.response

        TestCreateResponse.verify_response(self, res)

    @staticmethod
    def verify_response(tc, res):
        tc.assertEqual(TestDirectConceptMatches.N_MATCHES - 1, len(res["matches"]))  # only 2 unique matches
        tc.assertEqual(1, len(res["multi_matches"]))  # 'Ground Speed' and 'Ground Station'
        tc.assertTrue(4 in res["multi_matches"])  # 'GS' @ 4
        tc.assertEqual(TestEntityMatching.N_MATCHES, len(res["predicted_matches"]))  # TestEntityMatching checks correctness
        tc.assertEqual(1, len(res["undefined_entities"]))
        undefined_entity_artifact = res["undefined_entities"][0]
        tc.assertEqual(CONCEPT_ENTITY_UNDEFINED, undefined_entity_artifact[ArtifactKeys.ID])
