from gen_common.constants import EMPTY_STRING, NO_CHECK
from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.dataframes.layer_dataframe import LayerDataFrame
from gen_common.data.dataframes.trace_dataframe import TraceDataFrame
from gen_common.data.keys.structure_keys import StructuredKeys
from gen_common.data.readers.abstract_project_reader import AbstractProjectReader, TraceDataFramesTypes
from gen_common.data.readers.definitions.api_definition import ApiDefinition
from gen_common.util import DictUtil, EnumDict
from gen_common.util.json_util import JsonUtil


class ApiProjectReader(AbstractProjectReader[TraceDataFramesTypes]):
    """
    Responsible for converting JSON from API into DataFrames containing artifacts and traces.
    """

    def __init__(self, api_definition: ApiDefinition = None, project_path: str = EMPTY_STRING, overrides: dict = None):
        """
        Constructs project reader targeting given api.
        :param api_definition: The API payload containing artifacts and trace links.
        :param project_path: Ignored. Used to fulfill API.
        :param overrides: The parameters to override.
        """
        super().__init__(project_path=project_path, overrides=overrides)
        assert api_definition or project_path, "Must supply an api definition or project path"
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
        if self.get_full_project_path():
            api_dict = JsonUtil.read_json_file(self.get_full_project_path())
            self.api_definition = ApiDefinition.from_dict(**api_dict)
        artifact_df = self.create_artifact_df()
        layer_mapping_df = self.create_layer_df()
        trace_df = self.create_trace_df()

        if self.summarizer is not None:
            artifact_df.summarize_content(self.summarizer)

        return artifact_df, trace_df, layer_mapping_df

    def create_trace_df(self) -> TraceDataFrame:
        """
        Creates trace data frame containing links defined by API payload.
        :return: Trace data frame.
        """
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
        return ArtifactDataFrame(self.api_definition.artifacts)

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
    def create_layer_id(layer_name: str, layer_index: int) -> str:
        """
        Creates identifier for layer at index.
        :param layer_name: Either `source` or `target`
        :param layer_index: The index at which the layer is found.
        :return: The ID for the layer.
        """
        return f"{layer_name}_{str(layer_index)}"
