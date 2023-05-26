import os
from typing import Dict

from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.readers.abstract_project_reader import AbstractProjectReader, ProjectData, TraceDataFramesTypes
import pandas as pd


class DataFrameProjectReader(AbstractProjectReader[TraceDataFramesTypes]):
    """
    Reads projects exported by the DataFrameExporter
    """
    def __init__(self, project_path: str, artifact_df_filename: str = "artifact_df.csv", trace_df_filename: str = "trace_df.csv",
                 layer_df_filename: str = "layer_df.csv", overrides: dict = None):
        """
        Initializes the reader with the necessary information to the files containing each dataframe
        :param project_path: Base path to the project
        :param artifact_df_filename: Name of file containing artifact dataframe
        :param trace_df_filename: Name of file containing trace dataframe
        :param layer_df_filename: Name of file containing layer dataframe
        :param overrides: The overrides to apply to project creator.
        """
        super().__init__(overrides)
        self.project_path = project_path
        self.filename_to_dataframe_cls = {artifact_df_filename: ArtifactDataFrame,
                                          trace_df_filename: TraceDataFrame,
                                          layer_df_filename: LayerDataFrame}

    def read_project(self) -> TraceDataFramesTypes:
        """
        Reads in the project dataframes
        :return: The Project dataframes
        """
        dataframes = []
        for filename, dataframe_cls in self.filename_to_dataframe_cls.items():
            params = {"index_col": 0} if dataframe_cls.index_name() is None else {}
            df: pd.DataFrame = pd.read_csv(os.path.join(self.project_path, filename), **params)
            if self.summarizer:
                self.summarizer.summarize_dataframe(df, col2summarize=ArtifactKeys.CONTENT.value,
                                                    col2use4chunker=ArtifactKeys.LAYER_ID.value)
            dataframes.append(dataframe_cls(df))
        return tuple(dataframes)

    def get_project_name(self) -> str:
        """
        Returns the name of the project
        :return: The name of the project
        """
        return os.path.dirname(self.project_path)
