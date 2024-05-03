from unittest import TestCase

from test.concepts.constants import ConceptData
from test.concepts.test_entity_matching import TestEntityMatching
from test.concepts.utils import create_concept_args, create_concept_state
from tgen.concepts.steps.create_response_step import CreateResponseStep
from tgen.concepts.steps.direct_concept_matching_step import DirectConceptMatchingStep
from tgen.concepts.steps.entity_matching_step import EntityMatchingStep
from tgen.concepts.types.concept_pipeline_response import ConceptPipelineResponse
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


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
        state.entity_df = ConceptData.get_entity_df()
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
        tc.assertTrue(ConceptData.Expected.MULTI_MATCH_LOC in res["multi_matches"])
        tc.assertEqual(ConceptData.Expected.N_PREDICTED_MATCHES, len(res["predicted_matches"]))
        tc.assertEqual(ConceptData.Predicted[0], res["predicted_matches"][0])
        tc.assertEqual(ConceptData.Expected.N_UNDEFINED, len(res["undefined_entities"]))
        undefined_entity_artifact = res["undefined_entities"][0]
        tc.assertEqual(ConceptData.Entities.UNDEFINED, undefined_entity_artifact[ArtifactKeys.ID])
