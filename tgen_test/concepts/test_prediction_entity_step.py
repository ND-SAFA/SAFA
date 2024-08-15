from typing import List

from common_resources.data.keys.structure_keys import TraceKeys
from common_resources.mocking.mock_anthropic import mock_anthropic
from common_resources.mocking.test_response_manager import TestAIManager
from common_resources.tools.util.json_util import JsonUtil

from tgen.concepts.concept_state import ConceptState
from tgen.concepts.steps.predict_entity_step import PredictEntityStep
from tgen.testres.base_tests.base_test import BaseTest
from tgen_test.concepts.utils import create_concept_args


class TestPredictEntityStep(BaseTest):
    @mock_anthropic
    def test_use_case(self, ai_manager: TestAIManager) -> None:
        """
        Verifies that concepts are able to be predicted by model.
        ---
        Must verify that:
        - Each artifact is shown to model and predicted links are captured
        """
        # Step - Mock expected responses
        EXPECTED_MATCHES = ["C1"]
        ai_manager.add_responses([self._create_mock_response(EXPECTED_MATCHES), self._create_mock_response([])])

        # Step - Create pipeline resources
        args = create_concept_args()
        state = ConceptState()
        step = PredictEntityStep()

        step.run(args, state)

        matched_concepts = set([m[TraceKeys.TARGET] for m in state.predicted_matches])
        self.assertEqual(matched_concepts, set(EXPECTED_MATCHES))

    @staticmethod
    def _create_mock_response(concept_ids: List[str]) -> str:
        """
        Creates mock responses for concept matching predictions.
        :param concept_ids: List of Ids to predict.
        :return: Response.
        """
        return JsonUtil.dict_to_json({"predictions": concept_ids})
