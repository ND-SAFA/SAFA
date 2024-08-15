from common_resources.data.readers.abstract_project_reader import AbstractProjectReader
from common_resources.data.readers.repository_project_reader import RepositoryProjectReader
from tgen.testres.paths.project_paths import REPO_ONE_PROJECT_PATH
from tgen.testres.testprojects.abstract_test_project import AbstractTestProject


class RepositoryOneTestProject(AbstractTestProject):
    """
    Contains path and entries for repository project "one"
    """

    ARTIFACT_SET_INDEX = 0
    TRACE_RANGE = 3

    @staticmethod
    def get_project_path() -> str:
        """
        :return: Returns path to repository test project.
        """
        return REPO_ONE_PROJECT_PATH

    @classmethod
    def get_project_reader(cls) -> AbstractProjectReader:
        """
        :return: Returns repository project reader for project.
        """
        return RepositoryProjectReader(cls.get_project_path())

    @staticmethod
    def get_n_links() -> int:
        """
        :return: Returns the number of links with t3 removed.
        """
        return 6

    @classmethod
    def get_n_positive_links(cls) -> int:
        """
        :return: Returns the number of positive links in repository.
        """
        return 3
