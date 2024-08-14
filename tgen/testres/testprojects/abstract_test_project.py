from abc import abstractmethod
from typing import List

import numpy as np

from tgen.common.objects.artifact import Artifact
from tgen.common.objects.trace import Trace
from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.keys.structure_keys import StructuredKeys, TraceKeys
from common_resources.data.readers.abstract_project_reader import AbstractProjectReader
from tgen.common.objects.trace_layer import TraceLayer


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
    def get_source_artifacts(cls) -> List[Artifact]:
        """
        :return: Returns the source artifact entries per artifact layer.
        """
        return cls._get_artifacts_in_layer(StructuredKeys.LayerMapping.SOURCE_TYPE)

    @classmethod
    def get_target_artifacts(cls) -> List[Artifact]:
        """
        :return: Returns the target artifact entries per artifact layer.
        """
        return cls._get_artifacts_in_layer(StructuredKeys.LayerMapping.TARGET_TYPE)

    @classmethod
    def get_trace_entries(cls) -> List[Trace]:
        """
        :return: Returns trace entries in project.
        """
        project_reader = cls.get_project_reader()
        _, trace_df, _ = project_reader.read_project()
        entries = []
        for i, row in trace_df.iterrows():
            score = row.get(TraceKeys.SCORE.value, None)
            label = row.get(TraceKeys.LABEL.value, None)

            score = None if np.isnan(score) else score
            label = None if np.isnan(label) else label
            entry = Trace(
                source=row[TraceKeys.SOURCE.value],
                target=row[TraceKeys.TARGET.value],
                label=label,
                score=score
            )
            entries.append(entry)
        return entries

    @classmethod
    def get_trace_layers(cls) -> List[TraceLayer]:
        """
        :return: Returns layer mapping entries in project.
        """
        project_reader = cls.get_project_reader()
        artifact_df, trace_df, layer_df = project_reader.read_project()
        layers = []
        for layer_id, layer_row in layer_df.iterrows():
            parent_type = layer_row[StructuredKeys.LayerMapping.TARGET_TYPE.value]
            child_type = layer_row[StructuredKeys.LayerMapping.SOURCE_TYPE.value]
            layer = TraceLayer(parent=parent_type, child=child_type)
            layers.append(layer)
        return layers

    @classmethod
    def get_layer_entries(cls):
        layer_entries = [{StructuredKeys.LayerMapping.SOURCE_TYPE.value: l.child,
                          StructuredKeys.LayerMapping.TARGET_TYPE.value: l.parent}
                         for l in cls.get_trace_layers()]
        return layer_entries

    @classmethod
    def get_artifact_entries(cls) -> List[Artifact]:
        """
        :return: Returns artifact entries present in project.
        """
        return cls.get_source_artifacts() + cls.get_target_artifacts()

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
