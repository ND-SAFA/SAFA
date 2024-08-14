from unittest import TestCase

from tgen_test.concepts.constants import CONCEPT_R1, ConceptData
from tgen_test.concepts.test_entity_matching import TestEntityMatching
from tgen_test.concepts.utils import create_concept_args, create_concept_state
from tgen.concepts.steps.create_response_step import CreateResponseStep
from tgen.concepts.steps.direct_concept_matching_step import DirectConceptMatchingStep
from tgen.concepts.steps.entity_matching_step import EntityMatchingStep
from tgen.concepts.types.concept_pipeline_response import ConceptPipelineResponse
from tgen.testres.base_tests.base_test import BaseTest
from common_resources.mocking.mock_anthropic import mock_anthropic
from common_resources.mocking.test_response_manager import TestAIManager


class TestCreateResponse(BaseTest):
    @mock_anthropic
    def test_create_response(self, ai_manager: TestAIManager) -> None:
        """
        Tests the ability to create the final response for concept pipeline.
        :param ai_manager: AI manager used to mock entity matching.
        :return: None
        """
        args = create_concept_args()
        state = create_concept_state(args)

        # Mock pipeline execution assumptions
        DirectConceptMatchingStep().run(args, state)
        state.entity_data_frames = ConceptData.get_entity_dataframes()
        TestEntityMatching.mock_entity_matching(ai_manager)
        EntityMatchingStep().run(args, state)
        CreateResponseStep().run(args, state)

        res = state.response

        TestCreateResponse.verify_response(self, res)

    @staticmethod
    def verify_response(tc: TestCase, res: ConceptPipelineResponse) -> None:
        """
        Verifies that response matches expected test data.
        :param tc: Test case used to make assertions.
        :param res: Response to verify.
        :return: None
        """
        tc.assertEqual(ConceptData.Expected.N_DIRECT_MATCHES, len(res["matches"]))
        tc.assertEqual(ConceptData.Expected.N_MULTI_MATCHES, len(res["multi_matches"]))  # 'Ground Speed' and 'Ground Station'
        artifact_multi_matches = res["multi_matches"][CONCEPT_R1]
        tc.assertTrue(ConceptData.Expected.MULTI_MATCH_LOC in artifact_multi_matches)
        tc.assertEqual(ConceptData.Expected.N_PREDICTED_MATCHES, len(res["predicted_matches"]))
        tc.assertEqual(CONCEPT_R1, res["predicted_matches"][0]["target"])
        tc.assertEqual(ConceptData.Expected.N_UNDEFINED, len(res["undefined_entities"]))

        undefined_entity_lookup = {e["concept_id"]: e for e in res["undefined_entities"]}
        expected_undefined_entities = ConceptData.Entities.get_undefined_entities()

        for target_artifact_id, expected_undefined_entities in expected_undefined_entities:
            for e in expected_undefined_entities:
                tc.assertIn(e, undefined_entity_lookup)
                undefined_entity = undefined_entity_lookup[e]
                tc.assertIn(target_artifact_id, undefined_entity["artifact_ids"])
