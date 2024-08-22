from typing import List

from gen_common.data.keys.structure_keys import TraceKeys
from gen_common.util.json_util import JsonUtil
from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.tests.base_test import BaseTest

from gen.health.concepts.matching.concept_matching_state import ConceptMatchingState
from gen.health.concepts.matching.steps.llm_concept_matching_step import LLMConceptMatchingStep
from gen_test.health.concepts.matching.constants import ConceptData
from gen_test.health.concepts.matching.utils import create_concept_args


class TestLLMConceptMatchingStep(BaseTest):
    EXPECTED_MATCHES = [ConceptData.Entities.E2]

    @mock_anthropic
    def test_use_case(self, ai_manager: TestAIManager) -> None:
        """
        Verifies that:
        - Each artifact is shown to model (using specified number of prompts)
        - Predicted entities lead to trace links (using output)
        - Direct links are not shown to the model.
        """
        # Step - Mock expected responses
        self.mock_predictions(ai_manager)

        # Step - Create pipeline resources
        args = create_concept_args()
        state = ConceptMatchingState()
        step = LLMConceptMatchingStep()

        step.run(args, state)

    @staticmethod
    def verify_state(tc, state: ConceptMatchingState):
        matched_concepts = set([m[TraceKeys.TARGET] for m in state.predicted_matches])
        tc.assertEqual(matched_concepts, set(TestLLMConceptMatchingStep.EXPECTED_MATCHES))

    @staticmethod
    def mock_predictions(ai_manager: TestAIManager) -> None:
        ai_manager.add_responses([
            TestLLMConceptMatchingStep.create_mock_response(TestLLMConceptMatchingStep.EXPECTED_MATCHES),
            TestLLMConceptMatchingStep.create_mock_response([])]
        )

    @staticmethod
    def create_mock_response(
            concept_ids: List[str],
            explanations: List[str] = None,
            default_explanation: str = "explanation") -> str:
        """
        Creates mock responses for concept matching predictions.
        :param concept_ids: List of Ids to predict.
        :return: Response.
        """
        if explanations is None:
            explanations = [default_explanation for _ in concept_ids]
        return JsonUtil.dict_to_json({"predictions": [
            {"artifact_id": c_id, "explanation": c_e} for c_id, c_e in zip(concept_ids, explanations)
        ]})
