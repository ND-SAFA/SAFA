from typing import Dict, List
from unittest import TestCase

from tgen.common.objects.artifact import Artifact
from tgen.common.objects.trace import Trace
from tgen.data.keys.structure_keys import ArtifactKeys, TraceKeys
from tgen.tracing.ranking.common.ranking_util import RankingUtil


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
    def verify_order(tc: TestCase, expected_parent_predictions: Dict, resulting_predictions: List[Trace]) -> None:
        """
        Verifies the order of the trace links for each parent.
        :param tc: The test case to use to make assertions with.
        :param expected_parent_predictions: Map of parent to its ranked list of children.
        :param resulting_predictions: The predictions to verify the ranked order of children.
        :return: None.
        """
        resulting_parent2children = RankingUtil.group_trace_predictions(resulting_predictions, TraceKeys.parent_label())
        for parent_id, expected_children_ids in expected_parent_predictions.items():
            parent_preditions = sorted(resulting_parent2children[parent_id], key=lambda t: t["score"], reverse=True)
            for expected_artifact_id, prediction in zip(expected_children_ids, parent_preditions):
                predicted_artifact_id = prediction[TraceKeys.child_label()]
                tc.assertEqual(expected_artifact_id, predicted_artifact_id, msg=f"Parent: {parent_id}")
