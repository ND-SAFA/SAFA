from typing import Dict, List

from test.concepts.test_define_unknown_entities import TestDefineUnknownEntities
from test.concepts.test_entity_extraction import TestPredictEntityStep
from test.concepts.test_entity_matching import TestEntityMatching
from test.jobs.health_check_jobs.health_check_constants import ARTIFACT_CONTENT, ARTIFACT_IDS, CONCEPT_LAYER_ID, EXISTING_CONCEPTS, \
    EXPECTED_CONFLICTING_IDS, \
    EXPECTED_CONTEXT_IDS, EXPECTED_CONTRADICTION_EXPLANATION, EXPECTED_RELATED_ARTIFACTS, QUERY, QUERY_CONCEPTS, QUERY_CONTENT, \
    QUERY_ID, UNDEFINED_CONCEPT
from tgen.chat.message_meta import MessageMeta
from tgen.common.objects.artifact import Artifact
from tgen.common.util.enum_util import EnumDict
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys, TraceKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.prompts.supported_prompts.contradiction_prompts import create_contradiction_response
from tgen.testres.base_tests.base_test import BaseTest


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


def assert_health_check_success(tc: BaseTest, result: Dict):
    tc.assertEqual(1, len(result["contradictions"]))
    contradiction = result["contradictions"][0]
    tc.assertListEqual(contradiction["conflicting_ids"], EXPECTED_CONFLICTING_IDS + [QUERY_ID])
    tc.assertEqual(contradiction["explanation"], EXPECTED_CONTRADICTION_EXPLANATION)
    assert_correct_related_traces(tc, result["context_traces"], EXPECTED_RELATED_ARTIFACTS, QUERY_ID)

    concept_matches = result["concept_matches"]

    # Direct ("dog)
    direct_concept = EXISTING_CONCEPTS[0]
    tc.assertEqual(1, len(concept_matches["matches"]))
    direct_match = concept_matches["matches"][0]
    tc.assertEqual(direct_concept, direct_match["concept_id"])
    tc.assertEqual(direct_concept, direct_match["matched_content"])
    tc.assertEqual(QUERY_ID, direct_match["artifact_id"])

    # Predicted (pug)
    concept_id = EXISTING_CONCEPTS[0]
    entity_id = QUERY_CONCEPTS[0]
    tc.assertEqual(1, len(concept_matches["predicted_matches"]))
    predicted_match = concept_matches["predicted_matches"][0]
    tc.assertEqual(QUERY_ID, predicted_match["target"])
    tc.assertEqual(concept_id, predicted_match["source"])

    # Undefined (undefined_concept)
    tc.assertEqual(1, len(concept_matches["undefined_entities"]))
    undefined_entity = concept_matches["undefined_entities"][0]
    tc.assertEqual([QUERY_ID], undefined_entity["artifact_ids"])
    tc.assertEqual(UNDEFINED_CONCEPT, undefined_entity["concept_id"])


def get_dataset_for_context(include_query: bool = False):
    artifact_df = ArtifactDataFrame({ArtifactKeys.ID: ARTIFACT_IDS,
                                     ArtifactKeys.CONTENT: ARTIFACT_CONTENT,
                                     ArtifactKeys.LAYER_ID: "artifacts"})
    if include_query:
        artifact_df.add_row(QUERY)
    return PromptDataset(artifact_df=artifact_df)


def get_chat_history(artifact_ids: List = None):
    artifact_ids = [] if not artifact_ids else artifact_ids
    return [MessageMeta(message=AbstractLLMManager.convert_prompt_to_message(prompt=QUERY[ArtifactKeys.CONTENT]),
                        artifact_ids=artifact_ids)]


def get_dataset_for_health_checks():
    dataset = get_dataset_for_context()
    dataset.artifact_df.add_artifact(id=QUERY_ID,
                                     content=QUERY_CONTENT,
                                     layer_id="artifacts")
    for i, concept in enumerate(EXISTING_CONCEPTS):
        dataset.artifact_df.add_artifact(id=concept,
                                         content=concept,
                                         layer_id=CONCEPT_LAYER_ID)
    return dataset


@staticmethod
def mocks_for_health_checks(ai_manager):
    artifacts = [Artifact(id=e, content="description", layer_id="entity")
                 for e in QUERY_CONCEPTS]
    test_entity_df = ArtifactDataFrame(artifacts)
    ai_manager.add_responses([create_contradiction_response(EXPECTED_CONTRADICTION_EXPLANATION, EXPECTED_CONFLICTING_IDS)])
    TestPredictEntityStep.mock_entity_extraction(ai_manager, test_entity_df)
    TestEntityMatching.mock_entity_matching(ai_manager, [QUERY_CONCEPTS[1]] + ["NA"])
    mock_entity_definitions = {UNDEFINED_CONCEPT: "This is a new project concept"}
    TestDefineUnknownEntities.mock_entity_definitions(ai_manager, mock_entity_definitions)
