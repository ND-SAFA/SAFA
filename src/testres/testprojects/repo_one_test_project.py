from typing import Dict, List

from data.datasets.creators.readers.abstract_project_reader import AbstractProjectReader
from data.datasets.creators.readers.repository_project_reader import RepositoryProjectReader
from testres.paths.project_paths import REPO_ONE_PROJECT_PATH
from testres.test_data_manager import TestDataManager
from testres.testprojects.abstract_test_project import AbstractTestProject
from testres.testprojects.entry_creator import EntryCreator


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

    @classmethod
    def get_source_entries(cls) -> List[List[Dict]]:
        return EntryCreator.get_entries_in_type(TestDataManager.Keys.SOURCE, [cls.ARTIFACT_SET_INDEX])

    @classmethod
    def get_target_entries(cls) -> List[List[Dict]]:
        return EntryCreator.get_entries_in_type(TestDataManager.Keys.TARGET, [cls.ARTIFACT_SET_INDEX])

    def get_trace_entries(cls) -> List[Dict]:
        trace_data = TestDataManager.DATA[TestDataManager.Keys.TRACES][:cls.TRACE_RANGE]
        trace_data = [(a_id, a_body) for a_id, a_body in trace_data]
        return EntryCreator.create_trace_entries(trace_data)

    def get_layer_mapping_entries(cls) -> List[Dict]:
        return EntryCreator.create_layer_mapping_entries([("Commit", "Issue")])
