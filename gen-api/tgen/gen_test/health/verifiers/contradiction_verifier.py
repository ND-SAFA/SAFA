from typing import List, Tuple
from unittest import TestCase

from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common_test.base.mock.langchain.test_chat_model import TestResponseManager
from gen_common_test.base.mock.test_ai_manager import TestAIManager

from gen.health.contradiction.contradiction_graph import IdentifyContradictions
from gen.health.contradiction.contradiction_result import ContradictionResult
from gen.health.health_state import HealthState
from gen_test.health.health_check_constants import EXPECTED_CONFLICTING_IDS, EXPECTED_CONTRADICTION_EXPLANATION, QUERY_ID
from gen_test.health.health_check_utils import get_dataset_for_health_checks
from gen_test.health.health_task_verifier import HealthTaskVerifier


class ContradictionsVerifier(HealthTaskVerifier):
    def get_test_data(self) -> Tuple[PromptDataset, List[str]]:
        dataset = get_dataset_for_health_checks()
        query_ids = [QUERY_ID]
        return dataset, query_ids

    def mock_responses(self, ai_manager: TestAIManager, chat_ai_manager: TestResponseManager) -> None:
        chat_ai_manager.set_responses([IdentifyContradictions(contradiction_found=True,
                                                              explanation=EXPECTED_CONTRADICTION_EXPLANATION,
                                                              contradicting_ids=EXPECTED_CONFLICTING_IDS)])

    def verify_state(self, tc: TestCase, state: HealthState) -> None:
        tc.assertEqual(1, len(state.contradictions))
        contradiction: ContradictionResult = state.contradictions[0]
        tc.assertListEqual(contradiction.conflicting_ids, EXPECTED_CONFLICTING_IDS + [QUERY_ID])
        tc.assertEqual(contradiction.explanation, EXPECTED_CONTRADICTION_EXPLANATION)
