from typing import List, Dict

from test.concepts.test_entity_extraction import TestEntityExtraction
from test.concepts.test_entity_matching import TestEntityMatching
from tgen.common.objects.artifact import Artifact
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.prompt_util import PromptUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys, TraceKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.prompts.prompt import Prompt
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.testres.base_tests.base_test import BaseTest

ARTIFACT_CONTENT = ["All dogs are really cute.", "Car goes vroom.", "Fire trucks are loud.", "Dogs pee on fire hydrants.",
                    "Cats are better than Dogs"]
ARTIFACT_IDS = [f"a_{i}" for i in range(len(ARTIFACT_CONTENT))]
QUERY = Artifact(id="query1", content="What pet should I get?", layer_id="queries")
EXPECTED_CONTEXT_IDS = [ARTIFACT_IDS[0], ARTIFACT_IDS[-1]]
EXPECTED_CONTRADICTION = ARTIFACT_IDS[0]
EXISTING_CONCEPTS = ["dog", "cat", "fire truck", "car", "vroom"]
CONCEPT_LAYER_ID = "concept"
QUERY_CONCEPTS = ["pug", "dog"]
QUERY_CONTENT = "Pugs aren't cute dogs."
QUERY_ID = "target"
EXPECTED_RELATED_ARTIFACTS = EXPECTED_CONTEXT_IDS + EXISTING_CONCEPTS[:2]


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


def assert_health_check_success(test_case: BaseTest, result: Dict):
    test_case.assertListEqual(result["contradictions"]["conflicting_ids"], [EXPECTED_CONTRADICTION])
    assert_correct_related_traces(test_case, result["context_traces"], EXPECTED_RELATED_ARTIFACTS, QUERY_ID)
    direct_matches = [a[ArtifactKeys.ID.value] for a in result["concept_matches"]['matches']]
    undefined_matches = [a[ArtifactKeys.ID.value] for a in result["concept_matches"]['undefined_entities']]
    for concept in QUERY_CONCEPTS:
        if concept in EXISTING_CONCEPTS:
            test_case.assertIn(concept, direct_matches)
        else:
            test_case.assertIn(concept, undefined_matches)


def get_dataset_for_context(include_query: bool = False):
    artifact_df = ArtifactDataFrame({ArtifactKeys.ID: ARTIFACT_IDS,
                                     ArtifactKeys.CONTENT: ARTIFACT_CONTENT,
                                     ArtifactKeys.LAYER_ID: "artifacts"})
    if include_query:
        artifact_df.add_row(QUERY)
    return PromptDataset(artifact_df=artifact_df)


def get_dataset_for_health_checks():
    dataset = get_dataset_for_context()
    dataset.artifact_df.add_artifact(a_id=QUERY_ID,
                                     content=QUERY_CONTENT,
                                     layer_id="artifacts")
    for i, concept in enumerate(EXISTING_CONCEPTS):
        dataset.artifact_df.add_artifact(a_id=concept,
                                         content=concept,
                                         layer_id=CONCEPT_LAYER_ID)
    return dataset


@staticmethod
def mocks_for_health_checks(ai_manager):
    task_prompt: Prompt = SupportedPrompts.CONTRADICTIONS_TASK.value
    contradiction_response_tag = task_prompt.get_all_response_tags()[0]
    artifacts = [Artifact(id=e, content="description", layer_id="entity")
                 for e in QUERY_CONCEPTS]
    test_entity_df = ArtifactDataFrame(artifacts)
    ai_manager.set_responses([PromptUtil.create_xml(contradiction_response_tag, EXPECTED_CONTRADICTION)])
    TestEntityExtraction.mock_entity_extraction(ai_manager, test_entity_df)
    TestEntityMatching.mock_entity_matching(ai_manager, QUERY_CONCEPTS[:1])
