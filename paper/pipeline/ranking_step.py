import os

import pandas as pd

from paper.common.completion_util import complete_prompts
from paper.common.prompt_builder import PromptBuilder
from paper.pipeline.base import RankingStore, create_artifact_map
from paper.pipeline.sort_step import registered_sorters
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.readers.structured_project_reader import StructuredProjectReader


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


def create_ranking_prompts(s: RankingStore):
    project_path = s.project_path
    project_path = os.path.expanduser(project_path)
    project_reader = StructuredProjectReader(project_path)
    artifact_df, _, _ = project_reader.read_project()

    source_names, target_names = extract_prompt_artifacts(artifact_df)
    artifact_map = create_artifact_map(artifact_df)
    target_names = registered_sorters[s.sorter](source_names, target_names, artifact_map)  # sorts target names using sorter

    prompts = []
    for s_name in source_names:
        prompt = create_prompts(artifact_map, s_name, target_names, s)
        prompts.append(prompt)
    s.source_ids = source_names
    s.prompts = prompts


def create_prompts(artifact_map, source_name, target_names, s: RankingStore):
    query = artifact_map[source_name]
    prompt_builder = PromptBuilder(question=s.prompt_question, query=query, body_title="# Artifacts")
    for target_artifact_name in target_names:
        prompt_builder.with_artifact(target_artifact_name, artifact_map[target_artifact_name])
    prompt = prompt_builder.get()
    return prompt


def complete_ranking_prompts(s: RankingStore):
    batch_response = complete_prompts(s.prompts)
    s.batch_response = batch_response
