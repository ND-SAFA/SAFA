from typing import Dict

from tgen.common.util.dataframe_util import DataFrameUtil
from tgen.common.util.dict_util import DictUtil
from tgen.common.util.enum_util import EnumDict
from tgen.constants.dataset_constants import NO_CHECK
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.data.readers.abstract_project_reader import AbstractProjectReader, TraceDataFramesTypes
from tgen.data.readers.definitions.api_definition import ApiDefinition


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
        self.remove_orphans = False
        self.overrides = {
            "remove_orphans": False,
            "allowed_orphans": NO_CHECK,
            "allowed_missing_sources": 0,
            "allowed_missing_targets": 0
        }

    def read_project(self) -> TraceDataFramesTypes:
        """
        Extracts artifacts and trace links from API payload.
        :return: Artifacts, Traces, and Layer Mappings.
        """
        artifact_df = self.create_artifact_df()
        layer_mapping_df = self.create_layer_df()
        trace_df = self.create_trace_df()

        if self.summarizer is not None:
            artifact_df = self.summarizer.summarize_dataframe(artifact_df, col2summarize=StructuredKeys.Artifact.CONTENT.value,
                                                              col2use4chunker=StructuredKeys.Artifact.LAYER_ID.value)

        return artifact_df, trace_df, layer_mapping_df

    def create_trace_df(self):
        links = self.api_definition.get_links()
        trace_df_entries = []

        for trace_entry in links:
            trace_enum = DictUtil.create_trace_enum(trace_entry, StructuredKeys.Trace)
            trace_df_entries.append(trace_enum)
        trace_df = TraceDataFrame(trace_df_entries)
        return trace_df

    def create_artifact_df(self) -> ArtifactDataFrame:
        """
        Creates artifact data frame containing all layers of api definition.
        :return: Artifact data frame.
        """
        global_artifact_map = {}
        for artifact_type, artifact_map in self.api_definition.artifact_layers.items():
            global_artifact_map = self.add_artifact_layer(artifact_map, artifact_type, global_artifact_map)
        return ArtifactDataFrame(global_artifact_map)

    def create_layer_df(self) -> LayerDataFrame:
        """
        Create layer data frame from api definition.
        :return: Data frame containing layers being traced.
        """
        layer_mapping = []
        for layer in self.api_definition.layers:
            parent_type = layer.parent
            child_type = layer.child

            layer_mapping.append(EnumDict({
                StructuredKeys.LayerMapping.SOURCE_TYPE: child_type,
                StructuredKeys.LayerMapping.TARGET_TYPE: parent_type
            }))

        layer_mapping_df = LayerDataFrame(layer_mapping)
        return layer_mapping_df

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
