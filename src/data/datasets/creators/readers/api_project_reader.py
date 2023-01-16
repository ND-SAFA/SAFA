from typing import Dict, Tuple

import pandas as pd

from data.datasets.creators.readers.abstract_project_reader import AbstractProjectReader
from data.datasets.keys.structure_keys import StructureKeys
from server.api.api_definition import ApiDefinition


class ApiProjectReader(AbstractProjectReader):
    """
    Responsible for converting JSON from API into DataFrames containing artifacts and traces.
    """

    def __init__(self, api_definition: ApiDefinition):
        """
        Constructs project reader targeting given api.
        :param api_definition: The API payload containing artifacts and trace links.
        """
        self.api_definition = api_definition

    def read_project(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Extracts artifacts and trace links from API payload.
        :return: Artifacts, Traces, and Layer Mappings.
        """
        artifact_df = pd.DataFrame()
        trace_df = pd.DataFrame()
        layer_mapping_df = pd.DataFrame()

        source_layers = self.api_definition["source_layers"]
        target_layers = self.api_definition["target_layers"]
        links = self.api_definition["links"]

        for i, (source_layer, target_layer) in enumerate(zip(source_layers, target_layers)):
            source_layer_id = self._create_layer_id(StructureKeys.LayerMapping.SOURCE_TYPE, i)
            target_layer_id = self._create_layer_id(StructureKeys.LayerMapping.TARGET_TYPE, i)
            artifact_df = self.add_artifact_layer(source_layer, source_layer_id, artifact_df)
            artifact_df = self.add_artifact_layer(target_layer, target_layer_id, artifact_df)
            layer_mapping_df = layer_mapping_df.append({
                StructureKeys.LayerMapping.SOURCE_TYPE: source_layer_id,
                StructureKeys.LayerMapping.TARGET_TYPE: target_layer_id
            }, ignore_index=True)

        for source_id, target_id in links:
            trace_df = trace_df.append({
                StructureKeys.Trace.SOURCE: source_id,
                StructureKeys.Trace.TARGET: target_id,
                StructureKeys.Trace.LABEL: 1
            }, ignore_index=True)

        return artifact_df, trace_df, layer_mapping_df

    @staticmethod
    def add_artifact_layer(artifact_layer: Dict[str, str], layer_id: str, artifact_df: pd.DataFrame):
        """
        Adds series of artifacts in layer to artifact DataFrame.
        :param artifact_layer: Layer containing series of artifacts.
        :param layer_id: The id of the layer associated with the artifacts.
        :param artifact_df: DataFrame containing artifact aggregate.
        :return: Updated DataFrame containing new artifacts.
        """
        for t_id, t_body in artifact_layer.items():
            artifact_df = artifact_df.append({
                StructureKeys.Artifact.ID: t_id,
                StructureKeys.Artifact.BODY: t_body,
                StructureKeys.Artifact.LAYER_ID: layer_id
            }, ignore_index=True)
        return artifact_df

    @staticmethod
    def _create_layer_id(layer_name: str, layer_index: int) -> str:
        """
        Creates identifier for layer at index.
        :param layer_name: Either `source` or `target`
        :param layer_index: The index at which the layer is found.
        :return: The ID for the layer.
        """
        return f"{layer_name}_{str(layer_index)}"
