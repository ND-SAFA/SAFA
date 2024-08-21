from typing import List, Tuple

from gen_common_test.base.mock.decorators.chat import mock_chat_model
from gen_common_test.base.mock.langchain.test_chat_model import TestResponseManager
from gen_common_test.base.tests.base_test import BaseTest

from gen.health.contradiction.contradiction_args import ContradictionsArgs
from gen.health.contradiction.contradiction_detector import ContradictionsDetector
from gen.health.contradiction.contradiction_graph import IdentifyContradictions, NO_CONTRADICTIONS_RESPONSE
from gen.health.contradiction.contradiction_result import ContradictionResult
from gen_test.health.contradictions.data_test_requirements import EXPECTED_CONTRADICTIONS, get_contradictions_dataset


class TestContradictionsDetector(BaseTest):

    @mock_chat_model
    def test_detect_all(self, test_ai_manager: TestResponseManager):
        contradicting_id = "2"
        explanation = "This is why there is a contradiction."
        contradicting_ids = EXPECTED_CONTRADICTIONS[contradicting_id] + ["3"]

        args = ContradictionsArgs(dataset=get_contradictions_dataset())
        detector = ContradictionsDetector(args)

        test_ai_manager.set_responses([IdentifyContradictions(explanation=explanation,
                                                              contradicting_ids=contradicting_ids,
                                                              contradiction_found=True),
                                       IdentifyContradictions(contradiction_found=False),
                                       IdentifyContradictions(explanation=explanation,
                                                              contradiction_found=True)])
        conflicting_ids: List[str] = contradicting_ids + [contradicting_id]
        results = detector.detect([contradicting_id])
        self.verify_contradictions(results, [(explanation, conflicting_ids)])

        result = detector.detect(["1"])[0]
        self.assertEqual(result.explanation, NO_CONTRADICTIONS_RESPONSE)

        result = detector.detect(["1"])[0]
        self.assertEqual(result, None)

    def verify_contradictions(self, results: List[ContradictionResult],
                              expected: List[Tuple[str, List[str]]] = None) -> None:
        """
        Verifies the contradictions resulting from the detector.
        :param results: Results of the detection.
        :param expected: The expected results explanations and conflicting ids.
        :return: None
        """
        if not isinstance(expected, list):
            expected = [expected] if expected else []
        n_results = len(expected) if expected else 0

        for (explanation, conflicting_ids), result in zip(expected, results):
            self.assertEqual(result.conflicting_ids, conflicting_ids)
            self.assertEqual(result.explanation, explanation)
