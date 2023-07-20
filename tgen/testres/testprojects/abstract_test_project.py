from abc import abstractmethod
from typing import List

from tgen.common.artifact import Artifact
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.data.readers.abstract_project_reader import AbstractProjectReader
from tgen.ranking.common.trace_layer import TraceLayer
from tgen.train.trace_output.trace_prediction_output import TracePredictionEntry


class AbstractTestProject:
    """
    Represents interface for defining a test project to create assertions for.
    """

    @staticmethod
    @abstractmethod
    def get_project_path() -> str:
        """
        :return: Path to the test project.
        """

    @classmethod
    @abstractmethod
    def get_project_reader(cls) -> AbstractProjectReader:
        """
        :return: Returns project reader for project.
        """

    @classmethod
    def get_source_entries(cls) -> List[Artifact]:
        """
        :return: Returns the source artifact entries per artifact layer.
        """
        return cls._get_artifacts_in_layer(StructuredKeys.LayerMapping.SOURCE_TYPE)

    @classmethod
    def get_target_entries(cls) -> List[Artifact]:
        """
        :return: Returns the target artifact entries per artifact layer.
        """
        return cls._get_artifacts_in_layer(StructuredKeys.LayerMapping.TARGET_TYPE)

    @classmethod
    def get_trace_entries(cls) -> List[TracePredictionEntry]:
        """
        :return: Returns trace entries in project.
        """
        project_reader = cls.get_project_reader()
        _, trace_df, _ = project_reader.read_project()
        entries = []
        for i, row in trace_df.iterrows():
            entry = TracePredictionEntry(
                source=row[TraceKeys.SOURCE.value],
                target=row[TraceKeys.SOURCE.value],
                label=row.get(TraceKeys.LABEL.value, None),
                score=row.get(TraceKeys.SCORE.value, None)
            )
            entries.append(entry)
        return entries

    @classmethod
    def get_layer_mapping_entries(cls) -> List[TraceLayer]:
        """
        :return: Returns layer mapping entries in project.
        """
        project_reader = cls.get_project_reader()
        artifact_df, trace_df, layer_df = project_reader.read_project()
        layers = []
        for layer_id, layer_row in layer_df.iterrows():
            layer = TraceLayer(parent=layer_row[StructuredKeys.LayerMapping.TARGET_TYPE.value],
                               child=layer_row[StructuredKeys.LayerMapping.SOURCE_TYPE].value)
            layers.append(layer)
        return layers

    @classmethod
    def get_artifact_entries(cls) -> List[Artifact]:
        """
        :return: Returns artifact entries present in project.
        """
        return cls.get_source_entries() + cls.get_target_entries()

    @staticmethod
    @abstractmethod
    def get_n_links() -> int:
        """
        :return: Returns the number of expected links after construction.
        """

    @classmethod
    @abstractmethod
    def get_n_positive_links(cls) -> int:
        """
        :return: Returns the number of positive links in project.
        """

    @classmethod
    def _get_artifacts_in_layer(cls, layer: StructuredKeys.LayerMapping) -> List[Artifact]:
        """
        Returns the artifacts in given layer.
        :param layer: The layer key to extract artifacts with.
        :return: List of artifacts
        """
        project_reader = cls.get_project_reader()
        artifact_df, trace_df, layer_df = project_reader.read_project()
        source_types = list(layer_df[layer])
        layer_mask = artifact_df[StructuredKeys.Artifact.LAYER_ID].isin(source_types)
        source_df = ArtifactDataFrame(artifact_df[layer_mask])
        artifacts = source_df.to_artifacts()
        return artifacts
