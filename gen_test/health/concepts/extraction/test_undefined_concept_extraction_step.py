import json
from typing import List
from unittest import TestCase

from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.tests.base_test import BaseTest

from gen.health.concepts.concept_args import ConceptArgs
from gen.health.concepts.extraction.concept_extraction_state import ConceptExtractionState
from gen.health.concepts.extraction.steps.extract_undefined_concepts_step import ExtractUndefinedConceptsStep
from gen_test.health.concepts.extraction.concept_extraction_test_constants import TEST_HEALTH_CONCEPTS_EXTRACTION_EXISTING_CONCEPT, \
    TEST_HEALTH_CONCEPTS_EXTRACTION_UNDEFINED_CONCEPT
from gen_test.health.concepts.matching.constants import CONCEPT_R1, CONCEPT_R2
from gen_test.health.concepts.matching.utils import create_concept_args


class TestUndefinedConceptExtractionStep(BaseTest):

    @mock_anthropic
    def test_use_case(self, ai_manager: TestAIManager):
        """
        Verifies that UndefinedConceptExtractionStep:
        - Prompts LLM to extract undefined concepts
        - Will detect when LLM marked defined concept as undefined
        ---
        Inputs: ConceptData containing two query artifacts T1 and T2.
        Mock: One new concept for T1 and an existing concept for T2.
        Expected: Single undefined concept is identified and erroneous undefined entity is ignored.
        """
        self.mock_responses(ai_manager)

        args = create_concept_args()

        state = ConceptExtractionState()
        step = ExtractUndefinedConceptsStep()

        step.run(args, state)

        self.verify_state(self, state)

    @staticmethod
    def verify_state(tc: TestCase, state: ConceptExtractionState) -> None:
        """
        Verifies that state contains the expected end state of performing undefined concept extraction step.
        :param tc: The test case used to assert state.
        :param state: The state to verify.
        :return: None
        """
        tc.assertEqual(1, len(state.artifact2undefined[CONCEPT_R1]))
        tc.assertEqual(TEST_HEALTH_CONCEPTS_EXTRACTION_UNDEFINED_CONCEPT,
                       state.artifact2undefined[CONCEPT_R1][0])
        tc.assertEqual(0, len(state.artifact2undefined[CONCEPT_R2]))

    @classmethod
    def mock_responses(cls, ai_manager: TestAIManager) -> None:
        """
        Mocks responses for undefined concept extraction step.
        :param ai_manager: AI manager to add responses to.
        :return: None
        """
        ai_manager.add_responses([
            cls.create_mock_response([TEST_HEALTH_CONCEPTS_EXTRACTION_UNDEFINED_CONCEPT]),
            cls.create_mock_response([TEST_HEALTH_CONCEPTS_EXTRACTION_EXISTING_CONCEPT])
        ])

    @staticmethod
    def create_mock_response(undefined_concepts: List[str]) -> str:
        """
        Creates mock response for undefined concepts.
        :param undefined_concepts: List of undefined concepts.
        :return: Mock response.
        """
        return json.dumps({"undefined_concepts": undefined_concepts})

    @staticmethod
    def setup_data(args: ConceptArgs):
        """
        Performs data setup necessary to induce test case expected environment.
        :param args:
        :return:
        """
        args.dataset.trace_dataset.trace_df.add_link(CONCEPT_R2, TEST_HEALTH_CONCEPTS_EXTRACTION_EXISTING_CONCEPT)
