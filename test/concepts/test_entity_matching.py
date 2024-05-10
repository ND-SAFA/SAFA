from typing import List

from test.concepts.constants import ConceptData
from test.concepts.utils import create_concept_args, create_concept_state
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.str_util import StrUtil
from tgen.concepts.steps.entity_matching_step import EntityMatchingStep
from tgen.data.keys.structure_keys import ArtifactKeys
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
        direct_match_locs = [StrUtil.find_start_and_end_loc(args.artifact[ArtifactKeys.CONTENT], a_id, ignore_case=True)
                             for a_id in ConceptData.DirectMatches]
        state.direct_matches = [EnumDict({ArtifactKeys.ID: a_id,
                                          "start_loc": direct_match_locs[i][0],
                                          "end_loc": direct_match_locs[i][1]}) for i, a_id in enumerate(ConceptData.DirectMatches)]
        state.entity_df = ConceptData.get_entity_df()

        self.mock_entity_matching(ai_manager)
        step = EntityMatchingStep()
        step.run(args, state)

        predicted_links = state.predicted_matches
        self.assertEqual(TestEntityMatching.N_MATCHES, len(predicted_links))
        for i in range(TestEntityMatching.N_MATCHES):
            link = predicted_links[i]
            self.assertEqual(ConceptData.Predicted[i]["source"], link["source"])
            self.assertEqual(ConceptData.Predicted[i]["target"], link["target"])

    @staticmethod
    def mock_entity_matching(ai_manager: TestAIManager, matches: List = None) -> None:
        """
        Mocks response for entity matching.
        :param ai_manager: AI manager to add responses to.
        :return:None.
        """
        matches = [prediction["target"] for prediction in ConceptData.Predicted] + ["NA"] if not matches else matches
        responses = [EntityMatchingStep.create_example_xml(match) for match in matches]
        ai_manager.add_responses(responses)
