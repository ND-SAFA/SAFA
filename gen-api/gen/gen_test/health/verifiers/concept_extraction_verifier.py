from typing import List, Tuple
from unittest import TestCase

from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common_test.base.mock.langchain.test_chat_model import TestResponseManager
from gen_common_test.base.mock.test_ai_manager import TestAIManager

from gen.health.concepts.extraction.undefined_concept import UndefinedConcept
from gen.health.health_state import HealthState
from gen_test.health.concepts.extraction.concept_extraction_test_constants import TEST_HEALTH_CONCEPTS_EXTRACTION_MOCK_DEFINITION, \
    TEST_HEALTH_CONCEPTS_EXTRACTION_UNDEFINED_CONCEPT
from gen_test.health.concepts.extraction.test_define_undefined_concepts_step import TestDefineUndefinedConceptsStep
from gen_test.health.concepts.extraction.test_undefined_concept_extraction_step import TestUndefinedConceptExtractionStep
from gen_test.health.health_check_constants import QUERY_ID
from gen_test.health.health_check_utils import get_dataset_for_health_checks
from gen_test.health.health_task_verifier import HealthTaskVerifier


class ConceptExtractionVerifier(HealthTaskVerifier):

    def get_test_data(self) -> Tuple[PromptDataset, List[str]]:
        dataset = get_dataset_for_health_checks()
        query_ids = [QUERY_ID]
        return dataset, query_ids

    def mock_responses(self, ai_manager: TestAIManager, chat_manager: TestResponseManager) -> None:
        ai_manager.add_responses([
            TestUndefinedConceptExtractionStep.create_mock_response(
                TEST_HEALTH_CONCEPTS_EXTRACTION_UNDEFINED_CONCEPT
            ),
            TestDefineUndefinedConceptsStep.create_mock_response(
                TEST_HEALTH_CONCEPTS_EXTRACTION_MOCK_DEFINITION
            )
        ])

    def verify_state(self, tc: TestCase, state: HealthState) -> None:
        undefined_concepts = state.undefined_concepts
        tc.assertEqual(1, len(undefined_concepts))
        concept_match: UndefinedConcept = undefined_concepts[0]
        tc.assertEqual(TEST_HEALTH_CONCEPTS_EXTRACTION_UNDEFINED_CONCEPT, concept_match.concept_id)
