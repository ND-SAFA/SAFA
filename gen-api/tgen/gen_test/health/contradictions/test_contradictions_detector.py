from typing import List, Tuple

from gen_common_test.base.mock.decorators.chat import mock_chat_model
from gen_common_test.base.mock.langchain.test_chat_model import TestResponseManager
from gen_common_test.base.tests.base_test import BaseTest

from gen.health.contradiction.contradiction_graph import IdentifyContradictions, NO_CONTRADICTIONS_RESPONSE
from gen.health.contradiction.contradiction_pipeline import ContradictionPipeline
from gen.health.health_args import HealthArgs
from gen.health.health_state import HealthState
from gen_test.health.contradictions.data_test_requirements import EXPECTED_CONTRADICTIONS, get_contradictions_dataset


class TestContradictionsDetector(BaseTest):

    @mock_chat_model
    def test_detect_all(self, test_ai_manager: TestResponseManager):
        contradicting_id = "2"
        explanation = "This is why there is a contradiction."
        contradicting_ids = EXPECTED_CONTRADICTIONS[contradicting_id] + ["3"]

        test_ai_manager.set_responses([IdentifyContradictions(explanation=explanation,
                                                              contradicting_ids=contradicting_ids,
                                                              contradiction_found=True),
                                       IdentifyContradictions(contradiction_found=False),
                                       IdentifyContradictions(explanation=explanation,
                                                              contradiction_found=True)])
        conflicting_ids: List[str] = contradicting_ids + [contradicting_id]
        state = self.run_contradiction_pipeline([contradicting_id])
        self.verify_contradictions(state, [(explanation, conflicting_ids)])

        state = self.run_contradiction_pipeline(["1"])
        self.assertEqual(1, len(state.contradictions))
        self.assertEqual(state.contradictions[0].explanation, NO_CONTRADICTIONS_RESPONSE)

        state = self.run_contradiction_pipeline(["1"])
        self.assertEqual(state.contradictions, [None])

    @staticmethod
    def run_contradiction_pipeline(query_ids: List[str]) -> HealthState:
        args = HealthArgs(
            dataset=get_contradictions_dataset(),
            query_ids=query_ids
        )
        pipeline = ContradictionPipeline(args)
        pipeline.run()
        return pipeline.state

    def verify_contradictions(self, state: HealthState, expected: List[Tuple[str, List[str]]] = None) -> None:
        """
        Verifies the contradictions resulting from the detector.
        :param state: State of health checks.
        :param expected: The expected results explanations and conflicting ids.
        :return: None
        """
        results = state.contradictions
        if not isinstance(expected, list):
            expected = [expected] if expected else []
        n_results = len(expected) if expected else 0

        for (explanation, conflicting_ids), result in zip(expected, results):
            self.assertEqual(result.conflicting_ids, conflicting_ids)
            self.assertEqual(result.explanation, explanation)
