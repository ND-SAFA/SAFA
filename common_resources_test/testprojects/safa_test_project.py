from common_resources.data.readers.abstract_project_reader import AbstractProjectReader
from common_resources.data.readers.structured_project_reader import StructuredProjectReader
from common_resources_test.paths.project_paths import SAFA_PROJECT_PATH
from common_resources_test.testprojects.abstract_test_project import AbstractTestProject


class SafaTestProject(AbstractTestProject):
    """
    Contains safa test project testing details.
    """

    @staticmethod
    def get_n_links() -> int:
        return 18

    @classmethod
    def get_n_positive_links(cls) -> int:
        return 6

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
        return StructuredProjectReader(SAFA_PROJECT_PATH, overrides={
            "allowed_orphans": 2, "remove_orphans": False
        })
