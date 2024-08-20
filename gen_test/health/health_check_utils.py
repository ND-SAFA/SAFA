from typing import List

from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.dataframes.layer_dataframe import LayerDataFrame
from gen_common.data.dataframes.trace_dataframe import TraceDataFrame
from gen_common.data.keys.structure_keys import ArtifactKeys, TraceKeys
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.data.tdatasets.trace_dataset import TraceDataset
from gen_common.llm.abstract_llm_manager import AbstractLLMManager
from gen_common.llm.message_meta import MessageMeta
from gen_common.util.enum_util import EnumDict
from gen_common_test.base.tests.base_test import BaseTest

from gen.health.concepts.extraction.undefined_concept import UndefinedConcept
from gen.health.contradiction.contradiction_result import ContradictionResult
from gen.health.health_results import HealthResults
from gen_test.health.concepts.extraction.concept_extraction_test_constants import TEST_HEALTH_CONCEPTS_EXTRACTION_UNDEFINED_CONCEPT
from gen_test.health.health_check_constants import ARTIFACT_CONTENT, ARTIFACT_IDS, EXPECTED_CONFLICTING_IDS, \
    EXPECTED_CONTEXT_IDS, EXPECTED_CONTRADICTION_EXPLANATION, EXPECTED_RELATED_ARTIFACTS, QUERY, QUERY_ID


def assert_correct_related_artifacts(test_case: BaseTest, related_ids: List[str]):
    test_case.assertEqual(len(EXPECTED_CONTEXT_IDS), len(related_ids))
    for a_id in EXPECTED_CONTEXT_IDS:
        test_case.assertIn(a_id, related_ids)


def assert_correct_related_traces(test_case: BaseTest, related_traces: List[EnumDict], expected_context_ids=None,
                                  query_artifact=None):
    query_artifact = QUERY[ArtifactKeys.ID] if not query_artifact else query_artifact
    expected_context_ids = EXPECTED_CONTEXT_IDS if not expected_context_ids else expected_context_ids
    test_case.assertEqual(len(related_traces), len(expected_context_ids))
    for trace in related_traces:
        test_case.assertIn(trace[TraceKeys.parent_label().value], expected_context_ids)
        test_case.assertEqual(trace[TraceKeys.child_label().value], query_artifact)


def assert_health_check_success(tc: BaseTest, result: HealthResults):
    tc.assertEqual(1, len(result.contradictions))
    contradiction: ContradictionResult = result.contradictions[0]
    tc.assertListEqual(contradiction.conflicting_ids, EXPECTED_CONFLICTING_IDS + [QUERY_ID])
    tc.assertEqual(contradiction.explanation, EXPECTED_CONTRADICTION_EXPLANATION)
    assert_correct_related_traces(tc, result.context_traces, EXPECTED_RELATED_ARTIFACTS, QUERY_ID)

    concept_matches = result.undefined_concepts
    tc.assertEqual(1, len(concept_matches))
    concept_match: UndefinedConcept = concept_matches[0]
    tc.assertEqual(TEST_HEALTH_CONCEPTS_EXTRACTION_UNDEFINED_CONCEPT, concept_match.concept_id)


def get_chat_history(artifact_ids: List = None):
    artifact_ids = [] if not artifact_ids else artifact_ids
    return [MessageMeta(message=AbstractLLMManager.convert_prompt_to_message(prompt=QUERY[ArtifactKeys.CONTENT]),
                        artifact_ids=artifact_ids)]


def get_dataset_for_context(include_query: bool = False):
    artifact_df = ArtifactDataFrame({ArtifactKeys.ID: ARTIFACT_IDS,
                                     ArtifactKeys.CONTENT: ARTIFACT_CONTENT,
                                     ArtifactKeys.LAYER_ID: "artifacts"})
    if include_query:
        artifact_df.add_row(QUERY)
    trace_dataset = TraceDataset(
        artifact_df=artifact_df,
        trace_df=TraceDataFrame(),
        layer_df=LayerDataFrame()
    )
    return PromptDataset(trace_dataset=trace_dataset)
