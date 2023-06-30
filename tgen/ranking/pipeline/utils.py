import pandas as pd

from tgen.data.dataframes.artifact_dataframe import ArtifactKeys


def extract_prompt_artifacts(artifact_df: pd.DataFrame):
    """
    Extracts source and target artifact names.
    :param artifact_df: Artifact data frame containing ids, bodies, and types.
    :param n_sources: The number of artifacts in the source type.
    :return:
    """
    counts_df = artifact_df[ArtifactKeys.LAYER_ID.value].value_counts()
    n_sources = min(counts_df)
    source_type_name = counts_df[counts_df == n_sources].index[0]
    target_type_name = counts_df[counts_df != n_sources].index[0]

    source_df = artifact_df[artifact_df[ArtifactKeys.LAYER_ID.value] == source_type_name]
    target_df = artifact_df[artifact_df[ArtifactKeys.LAYER_ID.value] == target_type_name]

    source_artifact_names = list(source_df.index)
    target_artifact_names = list(target_df.index)
    return source_artifact_names, target_artifact_names
