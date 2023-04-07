from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.readers.abstract_project_reader import AbstractProjectReader
from tgen.data.readers.structured_project_reader import StructuredProjectReader


class ArtifactProjectReader(AbstractProjectReader[ArtifactDataFrame]):
    """
    Responsible for reading artifacts and trace links and constructing
    a trace dataset.
    """

    def __init__(self, project_path: str, conversions=None, overrides: dict = None):
        """
        Creates reader for project at path and column definitions given.
        :param project_path: Path to the project.
        :param conversions: Column definitions available to project.
        """
        super().__init__(overrides)
        self.structured_project_reader = StructuredProjectReader(project_path, conversions)

    def read_project(self) -> ArtifactDataFrame:
        """
        Reads project data from files.
        :return: Returns the data frames containing the project artifacts.
        """
        return self.structured_project_reader.read_artifact_df()

    def get_project_name(self) -> str:
        """
        Gets the name of the project being read.
        :return:  Returns the name of the project being read.
        """
        return self.structured_project_reader.get_project_name()
