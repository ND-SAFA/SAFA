from typing import List, Tuple
from unittest import TestCase

from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common_test.base.mock.langchain.test_chat_model import TestResponseManager
from gen_common_test.base.mock.test_ai_manager import TestAIManager

from gen.health.health_state import HealthState
from gen_test.health.concepts.matching.constants import ConceptData
from gen_test.health.concepts.matching.test_direct_concept_matching import TestDirectConceptMatching
from gen_test.health.concepts.matching.test_llm_concept_matching_step import TestLLMConceptMatchingStep
from gen_test.health.concepts.matching.utils import create_concept_dataset
from gen_test.health.health_task_verifier import HealthTaskVerifier


class ConceptMatchingVerifier(HealthTaskVerifier):
    def get_test_data(self) -> Tuple[PromptDataset, List[str]]:
        return create_concept_dataset()

    def mock_responses(self, ai_manager: TestAIManager, chat_manager: TestResponseManager) -> None:
        TestLLMConceptMatchingStep.mock_predictions(ai_manager)

    def verify_state(self, tc: TestCase, state: HealthState) -> None:
        TestDirectConceptMatching.verify_state(tc, state, ConceptData.DirectMatchesAfterMulti)
        TestLLMConceptMatchingStep.verify_state(tc, state)
