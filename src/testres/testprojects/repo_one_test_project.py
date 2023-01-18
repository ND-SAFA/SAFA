from typing import Dict, List

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

    @property
    def project_path(self) -> str:
        return REPO_ONE_PROJECT_PATH

    @classmethod
    def get_source_entries(cls) -> List[List[Dict]]:
        return EntryCreator.get_entries_in_type(TestDataManager.Keys.SOURCE, [cls.ARTIFACT_SET_INDEX])

    @classmethod
    def get_target_entries(cls) -> List[List[Dict]]:
        return EntryCreator.get_entries_in_type(TestDataManager.Keys.TARGET, [cls.ARTIFACT_SET_INDEX])

    def get_trace_entries(self) -> List[Dict]:
        trace_data = TestDataManager.DATA[TestDataManager.Keys.TRACES][:self.TRACE_RANGE]
        trace_data = [(a_id, a_body) for a_id, a_body in trace_data]
        return EntryCreator.create_trace_entries(trace_data)

    def get_layer_mapping_entries(self) -> List[Dict]:
        return EntryCreator.create_layer_mapping_entries([("Commit", "Issue")])
