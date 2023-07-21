from typing import List

from tgen.data.readers.dataframe_project_reader import DataFrameProjectReader
from tgen.testres.paths.project_paths import DATAFRAME_PROJECT_PATH
from tgen.testres.testprojects.abstract_test_project import AbstractTestProject
from tgen.testres.testprojects.entry_creator import LayerEntry


class DataFrameTestProject(AbstractTestProject):
    """
    Contains safa test project testing details.
    """

    @staticmethod
    def get_source_artifacts() -> List[LayerEntry]:
        raise NotImplementedError()

    @staticmethod
    def get_target_artifacts() -> List[LayerEntry]:
        raise NotImplementedError()

    @classmethod
    def get_trace_entries(cls) -> LayerEntry:
        raise NotImplementedError()

    @classmethod
    def get_trace_layers(cls) -> LayerEntry:
        raise NotImplementedError()

    @staticmethod
    def get_n_links() -> int:
        return 12

    @classmethod
    def get_n_positive_links(cls) -> int:
        return 6

    @staticmethod
    def get_project_path() -> str:
        """
        :return: Returns path to safa project.
        """
        return DATAFRAME_PROJECT_PATH

    @classmethod
    def get_project_reader(cls) -> DataFrameProjectReader:
        """
        :return: Returns structured project reader for project
        """
        return DataFrameProjectReader(project_path=DataFrameTestProject.get_project_path(),
                                      artifact_df_filename="artifact_df.csv",
                                      trace_df_filename="trace_df.csv",
                                      layer_df_filename="layer_df.csv",
                                      overrides={"allowed_orphans": 2, "remove_orphans": True})
