import os

import pandas as pd

from gen_common.constants.dataset_constants import ARTIFACT_FILE_NAME
from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.dataframes.layer_dataframe import LayerDataFrame
from gen_common.data.dataframes.trace_dataframe import TraceDataFrame
from gen_common.data.readers.abstract_project_reader import AbstractProjectReader, TraceDataFramesTypes
from gen_common.util.dict_util import DictUtil


class DataFrameProjectReader(AbstractProjectReader[TraceDataFramesTypes]):
    """
    Reads projects exported by the DataFrameExporter
    """

    def __init__(self, project_path: str, artifact_df_filename: str = ARTIFACT_FILE_NAME, trace_df_filename: str = "trace_df.csv",
                 layer_df_filename: str = "layer_df.csv", overrides: dict = None):
        """
        Initializes the reader with the necessary information to the files containing each dataframe
        :param project_path: Base path to the project
        :param artifact_df_filename: Name of file containing artifact dataframe
        :param trace_df_filename: Name of file containing trace dataframe
        :param layer_df_filename: Name of file containing layer dataframe
        :param overrides: The overrides to apply to project creator.
        """
        super().__init__(overrides, project_path)
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
            params = {}
            if dataframe_cls.index_name() is None:
                DictUtil.update_kwarg_values(params, index_col=0)
            df: pd.DataFrame = pd.read_csv(os.path.join(self.get_full_project_path(), filename), **params)
            df = dataframe_cls(df)
            if isinstance(df, ArtifactDataFrame) and self.summarizer:
                df.summarize_content(self.summarizer)
            dataframes.append(df)
        return tuple(dataframes)

    def get_project_name(self) -> str:
        """
        Returns the name of the project
        :return: The name of the project
        """
        return os.path.dirname(self.get_full_project_path())
