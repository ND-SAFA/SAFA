import json
from unittest import TestCase

from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.tests.base_test import BaseTest

from gen.health.concepts.extraction.concept_extraction_state import ConceptExtractionState
from gen.health.concepts.extraction.steps.define_undefined_concepts import DefineUndefinedConceptsStep
from gen_test.health.concepts.extraction.concept_extraction_test_constants import TEST_HEALTH_CONCEPTS_EXTRACTION_MOCK_DEFINITION, \
    TEST_HEALTH_CONCEPTS_EXTRACTION_UNDEFINED_CONCEPT
from gen_test.health.concepts.matching.constants import CONCEPT_R1
from gen_test.health.concepts.matching.utils import create_concept_args


class TestDefineUndefinedConceptsStep(BaseTest):

    @mock_anthropic
    def test_run(self, ai_manager: TestAIManager) -> None:
        """
        Tests the ability to create the final response for concept pipeline.
        :param ai_manager: AI manager used to mock entity matching.
        :return: None
        """
        self.mock_responses(ai_manager)

        args = create_concept_args()
        state = ConceptExtractionState()
        state.artifact2undefined = {CONCEPT_R1: [TEST_HEALTH_CONCEPTS_EXTRACTION_UNDEFINED_CONCEPT]}
        step = DefineUndefinedConceptsStep()

        step.run(args, state)

    @classmethod
    def verify_state(cls, tc: TestCase, state: ConceptExtractionState) -> None:
        """
        Asserts that state contains undefined concept.
        :param tc: Test case used to make assertions.
        :param state: State after the extraction step.
        :return: None
        """
        tc.assertEqual(1, len(state.undefined_concepts))
        undefined_concept = state.undefined_concepts[0]
        tc.assertEqual(TEST_HEALTH_CONCEPTS_EXTRACTION_UNDEFINED_CONCEPT, undefined_concept.concept_id)
        tc.assertIn(CONCEPT_R1, undefined_concept.artifact_ids)
        tc.assertEqual(TEST_HEALTH_CONCEPTS_EXTRACTION_MOCK_DEFINITION, undefined_concept.definition)

    @classmethod
    def mock_responses(cls, ai_manager: TestAIManager):
        """
        Mocks responses for unknown entity.
        :param ai_manager: AI manager to add responses to.
        :return: None
        """
        ai_manager.add_responses([
            cls.create_mock_response(TEST_HEALTH_CONCEPTS_EXTRACTION_MOCK_DEFINITION)
        ])

    @staticmethod
    def create_mock_response(definition: str) -> str:
        """
        Creates mock response for entity definition.
        :param definition: Definition used in mock response.
        :return: Mock response.
        """
        return json.dumps({"definition": definition})
