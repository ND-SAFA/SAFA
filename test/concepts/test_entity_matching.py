from typing import List

from test.concepts.constants import CONCEPT_R1, ConceptData
from test.concepts.utils import create_concept_args, create_concept_state
from tgen.concepts.steps.direct_concept_matching_step import DirectConceptMatchingStep
from tgen.concepts.steps.entity_matching_step import EntityMatchingStep
from tgen.concepts.types.entity_matching_context import EntityMatchingContext
from tgen.concepts.types.entity_matching_pred import EntityMatchingPred
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestEntityMatching(BaseTest):
    N_MATCHES = len(ConceptData.Predicted)

    @mock_anthropic
    def test_entity_matching(self, ai_manager: TestAIManager):
        """
        Tests that entities predicted
        :param ai_manager:
        :return:
        """
        args = create_concept_args()
        state = create_concept_state(args)

        DirectConceptMatchingStep().run(args, state)
        state.entity_data_frames = ConceptData.get_entity_dataframes()

        self.mock_entity_matching(ai_manager)
        step = EntityMatchingStep()
        step.run(args, state)

        predicted_links: List[EntityMatchingPred] = state.predicted_matches
        self.assertEqual(TestEntityMatching.N_MATCHES, len(predicted_links))
        for i in range(TestEntityMatching.N_MATCHES):
            link = predicted_links[i]
            self.assertEqual(CONCEPT_R1, link["artifact_id"])  # TODO: only works when single target artifact
            self.assertEqual(ConceptData.Predicted[i]["source"], link["entity_id"])
            self.assertEqual(ConceptData.Predicted[i]["target"], link["concept_id"])

    @staticmethod
    def mock_entity_matching(ai_manager: TestAIManager, matches: List = None) -> None:
        """
        Mocks response for entity matching.
        :param ai_manager: AI manager to add responses to.
        :param matches: Matches to override those in concept data.
        :return:None.
        """
        if not matches:
            matches = [prediction["target"] for prediction in ConceptData.Predicted] + ["NA"] * ConceptData.Expected.N_UNDEFINED
        responses = [match if match == "NA" else EntityMatchingContext.create_example_xml(match) for match in matches]
        ai_manager.add_responses(responses)
