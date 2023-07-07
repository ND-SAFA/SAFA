from typing import Any, Dict, Tuple, Type

from tgen.data.dataframes.abstract_project_dataframe import AbstractProjectDataFrame
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.util.enum_util import EnumDict

ArtifactKeys = StructuredKeys.Artifact


class ArtifactDataFrame(AbstractProjectDataFrame):
    """
    Contains the artifacts found in a project
    """

    @classmethod
    def index_name(cls) -> str:
        """
        Returns the name of the index of the dataframe
        :return: The name of the index of the dataframe
        """
        return ArtifactKeys.ID.value

    @classmethod
    def data_keys(cls) -> Type:
        """
        Returns the class containing the names of all columns in the dataframe
        :return: The class containing the names of all columns in the dataframe
        """
        return ArtifactKeys

    def add_artifact(self, artifact_id: Any, content: str, layer_id: Any = 1) -> EnumDict:
        """
        Adds artifact to dataframe
        :param artifact_id: The id of the Artifact
        :param content: The body of the artifact
        :param layer_id: The id of the layer that the artifact is part of
        :return: The newly added artifact
        """
        return self.add_new_row({ArtifactKeys.ID: artifact_id, ArtifactKeys.CONTENT: content,
                                 ArtifactKeys.LAYER_ID: layer_id})

    def get_artifact(self, artifact_id: Any) -> EnumDict:
        """
        Gets the row of the dataframe with the associated artifact_id
        :param artifact_id: The id of the artifact to get
        :return: The artifact if one is found with the specified params, else None
        """
        return self.get_row(artifact_id)

    def get_type(self, type_name: str):
        """
        Returns data frame with artifacts of given type.
        :param type_name: The type to filter by.
        :return: Artifacts in data frame of given type.
        """
        return self.filter_by_row(lambda r: r[ArtifactKeys.LAYER_ID.value] == type_name)

    def get_parent_child_types(self) -> Tuple[str, str]:
        """
        Returns the artifacts types of the parent and child artifacts.
        :return: Parent type and child type.
        """

        counts_df = self.get_type_counts()
        if len(counts_df) > 2:
            raise NotImplementedError("Multi-layer tracing is under construction.")
        n_sources = min(counts_df.values())
        parent_type = counts_df[counts_df == n_sources].index[0]
        child_type = counts_df[counts_df != n_sources].index[0]
        return parent_type, child_type

    def get_type_counts(self) -> Dict[str, str]:
        """
        Returns how many artifacts of each type exist in data frame.
        :return: map between type to number of artifacts of that type.
        """
        counts_df = self[ArtifactKeys.LAYER_ID].value_counts()
        type2count = dict(counts_df)
        return type2count

    def get_map(self) -> Dict[str, str]:
        """
        :return: Returns map of artifact ids to content.
        """
        artifact_map = {}
        for name, row in self.iterrows():
            content = row[ArtifactKeys.CONTENT.value]
            artifact_map[name] = content
        return artifact_map
