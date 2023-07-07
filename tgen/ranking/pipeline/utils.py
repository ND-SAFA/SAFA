from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame


def extract_prompt_artifacts(artifact_df: ArtifactDataFrame):
    """
    Extracts source and target artifact names.
    :param artifact_df: Artifact data frame containing ids, bodies, and types.
    :param n_sources: The number of artifacts in the source type.
    :return:
    """
    parent_type_name, children_type_name = artifact_df.get_parent_child_types()
    parent_df = artifact_df.get_type(parent_type_name)
    child_df = artifact_df.get_type(children_type_name)

    parent_names = list(parent_df.index)
    child_names = list(child_df.index)
    return parent_names, child_names
