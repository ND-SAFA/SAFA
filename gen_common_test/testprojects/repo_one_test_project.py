from gen_common.data.readers.abstract_project_reader import AbstractProjectReader
from gen_common.data.readers.repository_project_reader import RepositoryProjectReader
from gen_common_test.base.paths.project_paths import GEN_COMMON_TEST_PROJECT_REPO_ONE_PATH
from gen_common_test.testprojects.abstract_test_project import AbstractTestProject


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
        return GEN_COMMON_TEST_PROJECT_REPO_ONE_PATH

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
