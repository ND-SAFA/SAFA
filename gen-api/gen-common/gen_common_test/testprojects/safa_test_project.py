from gen_common.data.readers.abstract_project_reader import AbstractProjectReader
from gen_common.data.readers.structured_project_reader import StructuredProjectReader
from gen_common_test.base.paths.project_paths import GEN_COMMON_TEST_PROJECT_SAFA_PATH
from gen_common_test.testprojects.abstract_test_project import AbstractTestProject


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
        return GEN_COMMON_TEST_PROJECT_SAFA_PATH

    @classmethod
    def get_project_reader(cls) -> AbstractProjectReader:
        """
        :return: Returns structured project reader for project
        """
        return StructuredProjectReader(GEN_COMMON_TEST_PROJECT_SAFA_PATH, overrides={
            "allowed_orphans": 2, "remove_orphans": False
        })
