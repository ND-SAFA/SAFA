from typing import Dict, Tuple, Generic

import pandas as pd

from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.data.readers.abstract_project_reader import AbstractProjectReader, TraceDataFramesTypes
from tgen.server.api.api_definition import ApiDefinition
from tgen.util.dataframe_util import DataFrameUtil
from tgen.util.enum_util import EnumDict


class ApiProjectReader(AbstractProjectReader[TraceDataFramesTypes]):
    """
    Responsible for converting JSON from API into DataFrames containing artifacts and traces.
    """

    def __init__(self, api_definition: ApiDefinition, overrides: dict = None):
        """
        Constructs project reader targeting given api.
        :param api_definition: The API payload containing artifacts and trace links.
        :param overrides: The parameters to override.
        """
        super().__init__(overrides)
        self.api_definition = api_definition

    def read_project(self) -> TraceDataFramesTypes:
        """
        Extracts artifacts and trace links from API payload.
        :return: Artifacts, Traces, and Layer Mappings.
        """
        artifact_map = {}
        layer_mapping = []

        source_layers = self.api_definition.source_layers
        target_layers = self.api_definition.target_layers
        links = self.api_definition.get_links()

        for i, (source_layer, target_layer) in enumerate(zip(source_layers, target_layers)):
            source_layer_id = self.create_layer_id(StructuredKeys.LayerMapping.SOURCE_TYPE.value, i)
            target_layer_id = self.create_layer_id(StructuredKeys.LayerMapping.TARGET_TYPE.value, i)
            artifact_map = self.add_artifact_layer(source_layer, source_layer_id, artifact_map)
            artifact_map = self.add_artifact_layer(target_layer, target_layer_id, artifact_map)
            layer_mapping.append(EnumDict({
                StructuredKeys.LayerMapping.SOURCE_TYPE: source_layer_id,
                StructuredKeys.LayerMapping.TARGET_TYPE: target_layer_id
            }))

        trace_df_entries = []
        for source_id, target_id in links:
            trace_df_entries.append(EnumDict({
                StructuredKeys.Trace.SOURCE: source_id,
                StructuredKeys.Trace.TARGET: target_id,
                StructuredKeys.Trace.LABEL: 1
            }))

        artifact_df = ArtifactDataFrame(artifact_map)
        trace_df = TraceDataFrame(trace_df_entries)
        layer_mapping_df = LayerDataFrame(layer_mapping)
        return artifact_df, trace_df, layer_mapping_df

    def get_project_name(self) -> str:
        """
        :return: Under Construction. Currently, returns identifier that project is api request.
        """
        return "Api Request"

    @staticmethod
    def add_artifact_layer(artifact_layer: Dict[str, str], layer_id: str, artifact_map: Dict):
        """
        Adds series of artifacts in layer to artifact DataFrame.
        :param artifact_layer: Layer containing series of artifacts.
        :param layer_id: The id of the layer associated with the artifacts.
        :param artifact_map: Dictionary representing DataFrame containing artifact aggregate.
        :return: Updated dictionary containing new artifacts.
        """
        for t_id, t_body in artifact_layer.items():
            artifact_map = DataFrameUtil.append(artifact_map, EnumDict({
                StructuredKeys.Artifact.ID: t_id,
                StructuredKeys.Artifact.CONTENT: t_body,
                StructuredKeys.Artifact.LAYER_ID: layer_id
            }))
        return artifact_map

    @staticmethod
    def create_layer_id(layer_name: str, layer_index: int) -> str:
        """
        Creates identifier for layer at index.
        :param layer_name: Either `source` or `target`
        :param layer_index: The index at which the layer is found.
        :return: The ID for the layer.
        """
        return f"{layer_name}_{str(layer_index)}"
