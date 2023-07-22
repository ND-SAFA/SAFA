import pandas as pd

from tgen.data.dataframes.artifact_dataframe import ArtifactKeys


class DataStructureUtil:
    """
    Holds data structures for generic use.
    """

    @staticmethod
    def create_artifact_map(artifact_df: pd.DataFrame):
        """
        Creates map of artifact id to content.
        :param artifact_df: The data frame of artifacts.
        :return: Map of artifact id to content.
        """
        artifact_map = {}
        for artifact_index, artifact_row in artifact_df.iterrows():
            artifact_map[artifact_index] = artifact_row[ArtifactKeys.CONTENT.value]
        return artifact_map
