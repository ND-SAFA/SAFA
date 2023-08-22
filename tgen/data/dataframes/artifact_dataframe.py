from typing import Any, Dict, List, Type, Tuple

from tgen.common.artifact import Artifact
from tgen.common.util.dataframe_util import DataFrameUtil
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.override import overrides
from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.data.dataframes.abstract_project_dataframe import AbstractProjectDataFrame
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.summarizer.artifacts_summarizer import ArtifactsSummarizer

ArtifactKeys = StructuredKeys.Artifact


class ArtifactDataFrame(AbstractProjectDataFrame):
    """
    Contains the artifacts found in a project
    """

    OPTIONAL_COLUMNS = [StructuredKeys.Artifact.SUMMARY.value]
    _SUMMARY_DEFAULT = None

    @overrides(AbstractProjectDataFrame)
    def process_data(self) -> None:
        """
        Sets the index of the dataframe and performs any other processing steps
        :return: None
        """
        super().process_data()
        if not self.empty and StructuredKeys.Artifact.SUMMARY.value not in self.columns:
            self[StructuredKeys.Artifact.SUMMARY.value] = [self._SUMMARY_DEFAULT for _ in self.index]

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

    def add_artifact(self, artifact_id: Any, content: str, layer_id: Any = 1, summary: bool = EMPTY_STRING) -> EnumDict:
        """
        Adds artifact to dataframe
        :param artifact_id: The id of the Artifact
        :param content: The body of the artifact
        :param layer_id: The id of the layer that the artifact is part of
        :param summary: The summary of the artifact body
        :return: The newly added artifact
        """
        row_as_dict = {ArtifactKeys.ID: artifact_id, ArtifactKeys.CONTENT: content, ArtifactKeys.LAYER_ID: layer_id,
                       ArtifactKeys.SUMMARY: summary if summary else self._SUMMARY_DEFAULT}
        return self.add_new_row(row_as_dict)

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

    def get_type_counts(self) -> Dict[str, str]:
        """
        Returns how many artifacts of each type exist in data frame.
        :return: map between type to number of artifacts of that type.
        """
        counts_df = self[ArtifactKeys.LAYER_ID].value_counts()
        type2count = dict(counts_df)
        return type2count

    def to_map(self) -> Dict[str, str]:
        """
        :return: Returns map of artifact ids to content.
        """
        artifact_map = {}
        for name, row in self.itertuples():
            content = DataFrameUtil.get_optional_value(row, ArtifactKeys.SUMMARY)
            if content is None or len(content) == 0:
                content = row[ArtifactKeys.CONTENT]
            artifact_map[name] = content
        return artifact_map

    def to_artifacts(self) -> List[Artifact]:
        """
        Converts entries in data frame to converts.
        :return: The list of artifacts.
        """
        artifacts = [Artifact(id=artifact_id,
                              content=artifact_row[StructuredKeys.Artifact.CONTENT])
                     for artifact_id, artifact_row in self.itertuples()]
        return artifacts

    def get_body(self, artifact_id: str) -> str:
        """
        Retrieves the body of the artifact with given ID.
        :param artifact_id: The ID of the artifact.
        :return: The content of the artifact.
        """
        return self.loc[artifact_id][ArtifactKeys.CONTENT.value]

    def set_body(self, artifact_id: str, new_body: str) -> None:
        """
        Sets the body of the artifact with given ID.
        :param artifact_id: The id of the artifact.
        :param new_body: The body to update the artifact with.
        :return: None 
        """
        self.loc[artifact_id][ArtifactKeys.CONTENT.value] = new_body

    def summarize_content(self, summarizer: ArtifactsSummarizer) -> List[str]:
        """
        Summarizes the content in the artifact df
        :param summarizer: The summarizer to use
        :return: The summaries
        """
        if self[ArtifactKeys.SUMMARY.value].isna().any():
            missing_all = self[ArtifactKeys.SUMMARY].isna().all()
            if missing_all:
                summaries = summarizer.summarize_dataframe(self, ArtifactKeys.CONTENT.value, ArtifactKeys.ID.value)
                self[ArtifactKeys.SUMMARY] = summaries
            else:
                ids, content = self._find_missing_summaries()
                summaries = summarizer.summarize_bulk(bodies=content, filenames=ids)
                self.update_values(ArtifactKeys.SUMMARY, ids, summaries)
        return self[ArtifactKeys.SUMMARY]

    def _find_missing_summaries(self) -> Tuple[List, List]:
        """
        Finds artifacts that are missing summaries
        :return: The ids and content of the missing summaries
        """
        ids = []
        content = []
        for i, artifact in self.itertuples():
            if not artifact[ArtifactKeys.SUMMARY]:
                ids.append(i)
                content.append(artifact[ArtifactKeys.CONTENT])
        return ids, content

