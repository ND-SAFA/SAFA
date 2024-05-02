from typing import List

from tgen.common.objects.artifact import Artifact
from tgen.common.util.enum_util import EnumDict
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys, TraceKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.testres.base_tests.base_test import BaseTest

ARTIFACT_CONTENT = ["All dogs are really cute.", "Car goes vroom.", "Fire trucks are loud.", "Dogs pee on fire hydrants.",
                    "Cats are better than Dogs"]
ARTIFACT_IDS = [f"a_{i}" for i in range(len(ARTIFACT_CONTENT))]
QUERY = Artifact(id="query1", content="What pet should I get?", layer_id="queries")
EXPECTED_CONTEXT_IDS = [ARTIFACT_IDS[0], ARTIFACT_IDS[-1]]


def assert_correct_related_artifacts(test_case: BaseTest, related_artifacts: List[EnumDict]):
    related_ids = [a[ArtifactKeys.ID] for a in related_artifacts]
    test_case.assertEqual(len(EXPECTED_CONTEXT_IDS), len(related_ids))
    for a_id in EXPECTED_CONTEXT_IDS:
        test_case.assertIn(a_id, related_ids)


def assert_correct_related_traces(test_case: BaseTest, related_traces: List[EnumDict], expected_context_ids=None,
                                  query_artifact=None):
    query_artifact = QUERY[ArtifactKeys.ID] if not query_artifact else query_artifact
    expected_context_ids = EXPECTED_CONTEXT_IDS if not expected_context_ids else expected_context_ids
    test_case.assertEqual(len(related_traces), len(expected_context_ids))
    for trace in related_traces:
        test_case.assertIn(trace[TraceKeys.parent_label()], expected_context_ids)
        test_case.assertEqual(trace[TraceKeys.child_label()], query_artifact)


def get_dataset_for_context(include_query: bool = False):
    artifact_df = ArtifactDataFrame({ArtifactKeys.ID: ARTIFACT_IDS,
                                     ArtifactKeys.CONTENT: ARTIFACT_CONTENT,
                                     ArtifactKeys.LAYER_ID: "artifacts"})
    if include_query:
        artifact_df.add_row(QUERY)
    return PromptDataset(artifact_df=artifact_df)
