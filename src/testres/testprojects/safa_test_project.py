from data.datasets.creators.readers.abstract_project_reader import AbstractProjectReader
from data.datasets.creators.readers.structured_project_reader import StructuredProjectReader
from testres.paths.project_paths import SAFA_PROJECT_PATH
from testres.testprojects.api_test_project import ApiTestProject


class SafaTestProject(ApiTestProject):
    """
    Contains safa test project testing details.
    """

    @staticmethod
    def get_project_path() -> str:
        """
        :return: Returns path to safa project.
        """
        return SAFA_PROJECT_PATH

    @classmethod
    def get_project_reader(cls) -> AbstractProjectReader:
        """
        :return: Returns structured project reader for project
        """
        return StructuredProjectReader(SAFA_PROJECT_PATH)
