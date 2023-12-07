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
                test_case.assertEqual(expected_artifact[a_key], resulting_artifact[a_key.value])

    @staticmethod
    def verify_order(tc: TestCase, predictions: List[Trace], parent2sorted_children: Dict) -> None:
        """
        Verifies the order of the trace links for each parent.
        :param tc: The test case to use to make assertions with.
        :param predictions: The predictions to verify the ranked order of children.
        :param parent2sorted_children: Map of parent to its ranked list of children.
        :return: None.
        """
        parent2children = RankingUtil.group_trace_predictions(predictions, TraceKeys.parent_label())
        for parent_id, artifact_ids in parent2sorted_children.items():
            parent_predictions = parent2children[parent_id]
            sorted_parent_predictions = sorted(parent_predictions, key=lambda t: t["score"], reverse=True)
            for t_prediction, a_id in zip(sorted_parent_predictions, artifact_ids):
                tc.assertEqual(a_id, t_prediction[TraceKeys.child_label()])
