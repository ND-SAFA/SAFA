import json
from unittest import TestCase

from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.tests.base_test import BaseTest

from gen.health.concepts.extraction.concept_extraction_state import ConceptExtractionState
from gen.health.concepts.extraction.steps.condense_undefined_concepts import CondenseUndefinedConceptsStep
from gen_test.health.concepts.matching.utils import create_concept_args


class TestCondenseUndefinedConcepts(BaseTest):

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
        state.artifact2undefined = {
            "A1": ["term_1", "term_3"],
            "A2": ["term_2"]
        }
        step = CondenseUndefinedConceptsStep()

        step.run(args, state)

        self.verify_state(self, state)

    @classmethod
    def verify_state(cls, tc: TestCase, state: ConceptExtractionState) -> None:
        """
        Asserts that state contains undefined concept.
        :param tc: Test case used to make assertions.
        :param state: State after the extraction step.
        :return: None
        """
        tc.assertEqual(2, len(state.undefined_concepts))

        uc_1 = state.undefined_concepts[0]
        tc.assertEqual("base_term_1", uc_1.concept_id)
        tc.assertEqual(["A1", "A2"], uc_1.artifact_ids)

        uc_2 = state.undefined_concepts[1]
        tc.assertEqual("base_term_2", uc_2.concept_id)
        tc.assertEqual(["A1"], uc_2.artifact_ids)

    @classmethod
    def mock_responses(cls, ai_manager: TestAIManager):
        """
        Mocks responses for unknown entity.
        :param ai_manager: AI manager to add responses to.
        :return: None
        """
        response_obj = {
            "base_term_1": ["term_1", "term_2"],
            "base_term_2": ["term_3"]
        }
        ai_manager.add_responses([
            json.dumps(response_obj)
        ])
