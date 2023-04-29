from tgen.data.readers.abstract_project_reader import AbstractProjectReader
from tgen.data.readers.dataframe_project_reader import DataFrameProjectReader
from tgen.data.readers.structured_project_reader import StructuredProjectReader
from tgen.testres.paths.project_paths import DATAFRAME_PROJECT_PATH
from tgen.testres.testprojects.api_test_project import ApiTestProject


class DataFrameTestProject(ApiTestProject):
    """
    Contains safa test project testing details.
    """

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
