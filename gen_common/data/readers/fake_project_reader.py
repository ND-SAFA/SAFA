import uuid

from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.dataframes.layer_dataframe import LayerDataFrame
from gen_common.data.dataframes.trace_dataframe import TraceDataFrame
from gen_common.data.readers.abstract_project_reader import AbstractProjectReader, TraceDataFramesTypes


class FakeProjectReader(AbstractProjectReader[TraceDataFramesTypes]):
    """
    Can be used in place of a project reader when the dataframes are already created
    """

    def __init__(self, artifact_df: ArtifactDataFrame, layer_df: LayerDataFrame, trace_df: TraceDataFrame = None,
                 overrides: dict = None):
        """
        Initializes the reader with the pre-created dataframes
        :param artifact_df: Contains the artifacts
        :param trace_df: Contains the traces
        :param layer_df: Contains the layer mappings
        :param overrides: The overrides to apply to project creator.
        """
        super().__init__(overrides)
        self.artifact_df = artifact_df
        self.layer_df = layer_df
        self.trace_df = trace_df if trace_df else TraceDataFrame()

    def read_project(self) -> TraceDataFramesTypes:
        """
        Reads in the project dataframes
        :return: The Project dataframes
        """
        if self.summarizer:
            self.artifact_df.summarize_content(self.summarizer)
        dataframes = [self.artifact_df, self.trace_df, self.layer_df]
        return tuple(dataframes)

    def get_project_name(self) -> str:
        """
        Returns the name of the project
        :return: The name of the project
        """
        return str(uuid.uuid4())
