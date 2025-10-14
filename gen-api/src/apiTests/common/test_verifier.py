from typing import Dict, List
from unittest import TestCase

from gen_common.data.keys.structure_keys import ArtifactKeys, TraceKeys
from gen_common.data.objects.artifact import Artifact
from gen_common.data.objects.trace import Trace
from gen_common.util.ranking_util import RankingUtil


class TestVerifier:
    @staticmethod
    def assert_all_in(test_case: TestCase, text: str, items: List[str]) -> None:
        """
        Asserts that all items are contained in the text given.
        :param test_case: The test case used to assert containment.
        :param text: The text expected to contain items.
        :param items: The substrings expected to be in text.
        :return: None
        """
        for section_body in items:
            test_case.assertIn(section_body, text)

    @staticmethod
    def verify_artifacts(test_case: TestCase, artifacts: List[Artifact], resulting_artifacts: List[Dict],
                         ignore_keys: List[ArtifactKeys] = None) -> None:
        """
        Verifies that resulting artifacts match those expected for artifact keys.
        :param test_case: The test case used to make assertions.
        :param artifacts: The ground-truth artifacts.
        :param resulting_artifacts: The artifacts to verify.
        :param ignore_keys: The artifact keys to ignore comparing against existing.
        :return: None
        """
        if ignore_keys is None:
            ignore_keys = []
        resulting_artifact_map = {a[ArtifactKeys.ID.value]: a for a in resulting_artifacts}
        expected_artifact_map = {a[ArtifactKeys.ID]: a for a in artifacts}

        resulting_keys = set(resulting_artifact_map.keys())
        expected_keys = set(expected_artifact_map.keys())

        test_case.assertEqual(resulting_keys, expected_keys)

        for a_id in expected_keys:
            expected_artifact = expected_artifact_map[a_id]
            resulting_artifact = resulting_artifact_map[a_id]

            for a_key in ArtifactKeys:
                if a_key in ignore_keys:
                    continue
                e_value = expected_artifact[a_key]
                r_value = resulting_artifact[a_key.value]

                e_value = e_value.strip() if isinstance(e_value, str) else e_value
                r_value = r_value.strip() if isinstance(r_value, str) else r_value
                test_case.assertEqual(e_value, r_value, msg=f"{r_value}\n\nEXPECTED VALUE\n\n{e_value}")

    @staticmethod
    def verify_order(tc: TestCase, expected_parent_predictions: Dict, resulting_predictions: List[Trace], msg_suffix="") -> None:
        """
        Verifies the order of the trace links for each parent.
        :param tc: The test case to use to make assertions with.
        :param expected_parent_predictions: Map of parent to its ranked list of children.
        :param resulting_predictions: The predictions to verify the ranked order of children.
        :param msg_suffix:
        :return: None.
        """
        resulting_parent2children = RankingUtil.group_trace_predictions(resulting_predictions, TraceKeys.parent_label())
        for parent_id, expected_children_ids in expected_parent_predictions.items():
            parent_predictions = sorted(resulting_parent2children[parent_id], key=lambda t: t["score"], reverse=True)
            predicted_ids = [p[TraceKeys.child_label()] for p in parent_predictions]
            parent_msg = ",".join(expected_children_ids)
            received_msg = ",".join(predicted_ids)
            received_display = ",".join([TestVerifier.display_trace(p) for p in parent_predictions])
            tc.assertEqual(parent_msg, received_msg, msg=f"\n\nHashes did not match.\n{parent_msg}\n\n{received_display}{msg_suffix}")

    @staticmethod
    def display_trace(trace: Trace) -> str:
        """
        Creates display string of trace containing key and score.
        :param trace: The trace to represent.
        :return: String representation of the trace.
        """
        score = trace[TraceKeys.SCORE]
        child = trace[TraceKeys.child_label()]
        return f"{child}({round(score, 2)})"
