import pandas as pd

from paper.common.completion_util import complete_prompts
from paper.common.ranking_prompt_builder import RankingPromptBuilder
from paper.pipeline.base import RankingStore
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys


def extract_prompt_artifacts(artifact_df: pd.DataFrame, n_sources: int = 5):
    """
    Extracts source and target artifact names.
    :param artifact_df: Artifact data frame containing ids, bodies, and types.
    :param n_sources: The number of artifacts in the source type.
    :return:
    """
    counts_df = artifact_df[ArtifactKeys.LAYER_ID.value].value_counts()
    source_type_name = counts_df[counts_df == n_sources].index[0]
    target_type_name = counts_df[counts_df != n_sources].index[0]

    source_df = artifact_df[artifact_df[ArtifactKeys.LAYER_ID.value] == source_type_name]
    target_df = artifact_df[artifact_df[ArtifactKeys.LAYER_ID.value] == target_type_name]

    source_artifact_names = list(source_df.index)
    target_artifact_names = list(target_df.index)
    return source_artifact_names, target_artifact_names


def create_trace_queries(entries):
    entry_map = {}
    for entry in entries:
        source = entry["source"]
        target = entry["target"]
        if source not in entry_map:
            entry_map[source] = []
        entry_map[source].append(target)
    return entry_map


def create_ranking_prompts(s: RankingStore):
    artifact_map = s.artifact_map
    source2targets = s.source2targets
    source_names = s.source_ids

    prompts = []
    for s_name in source_names:
        prompt = create_prompts(artifact_map, s_name, s)
        prompts.append(prompt)

    s.prompts = prompts


def create_prompts(artifact_map, source_name, s: RankingStore):
    target_names = s.source2targets[source_name]
    query = artifact_map[source_name]
    prompt_builder = RankingPromptBuilder(question=s.prompt_question, format=s.prompt_format, query=query, body_title="# Artifacts")
    for target_index, target_artifact_name in enumerate(target_names):
        prompt_builder.with_artifact(target_index, artifact_map[target_artifact_name])
    prompt = prompt_builder.get()
    return prompt


def complete_ranking_prompts(s: RankingStore):
    batch_response = complete_prompts(s.prompts, max_tokens=2000)
    # batch_response = GenerationResponse(["<links>2,31,84,59,58,22,32,40</links>"] * len(s.prompts))
    s.batch_response = batch_response
