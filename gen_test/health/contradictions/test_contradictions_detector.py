from typing import List, Tuple

from gen_common.data.keys.structure_keys import TraceKeys, TraceRelationshipType
from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.tests.base_test import BaseTest

from gen.health.contradiction.contradiction_args import ContradictionsArgs
from gen.health.contradiction.contradiction_detector import ContradictionsDetector
from gen.health.contradiction.contradiction_prompts import create_contradiction_response
from gen_test.health.contradictions.data_test_requirements import EXPECTED_CONTRADICTIONS, get_contradictions_dataset


class TestContradictionsDetector(BaseTest):

    @mock_anthropic
    def test_detect_all(self, test_ai_manager: TestAIManager):
        contradicting_id = "2"
        explanation = "This is why there is a contradiction."
        contradicting_ids = EXPECTED_CONTRADICTIONS[contradicting_id] + ["3", "bad id"]

        args = ContradictionsArgs(dataset=get_contradictions_dataset())
        detector = ContradictionsDetector(args)

        test_ai_manager.add_responses([create_contradiction_response(explanation, contradicting_ids)])
        conflicting_ids: List[str] = EXPECTED_CONTRADICTIONS[contradicting_id] + [contradicting_id]
        self.verify_contradictions(detector, [contradicting_id], [(explanation, conflicting_ids)])

        # check related context added to trace dataframe
        context_link = args.dataset.trace_dataset.trace_df.get_link(source_id=contradicting_id,
                                                                    target_id=EXPECTED_CONTRADICTIONS[contradicting_id][0])
        self.assertIsNotNone(context_link)
        self.assertEqual(context_link[TraceKeys.RELATIONSHIP_TYPE], TraceRelationshipType.CONTEXT)

        test_ai_manager.add_responses(["No contradictions found"])
        self.verify_contradictions(detector, ["1"])

    def verify_contradictions(self, detector: ContradictionsDetector, query_ids: List[str],
                              expected: List[Tuple[str, List[str]]] = None) -> None:
        """
        Verifies the contradictions resulting from the detector.
        :param detector: The detector used to find contradictions.
        :param query_ids: Query IDs to find contradictions for.
        :param expected: The expected results explanations and conflicting ids.
        :return: None
        """
        if not isinstance(expected, list):
            expected = [expected] if expected else []
        n_results = len(expected) if expected else 0
        results = detector.detect(query_ids)
        self.assertEqual(len(results), n_results, msg=f"Query Ids: {query_ids}")

        for (explanation, conflicting_ids), result in zip(expected, results):
            self.assertEqual(result["conflicting_ids"], conflicting_ids)
            self.assertEqual(result["explanation"], explanation)
