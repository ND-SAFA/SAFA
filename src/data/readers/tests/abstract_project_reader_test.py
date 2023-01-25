from typing import Dict, List

from testres.base_test import BaseTest
from testres.test_assertions import TestAssertions
from testres.testprojects.abstract_test_project import AbstractTestProject


class AbstractProjectReaderTest(BaseTest):
    """
    Tests that project reader is able to construct dataset frames from project data.
    """

    def verify_project_data_frames(self, test_project: AbstractTestProject) -> None:
        """
        Verifies that entries are found in data frames created by project reader.
        :param test_project: Project containing entities to compare data frames to.
        :return: None
        """
        project_reader = test_project.get_project_reader()
        artifact_df, trace_df, layer_mapping_df = project_reader.read_project()
        TestAssertions.verify_entities_in_df(self, test_project.get_artifact_entries(), artifact_df)
        TestAssertions.verify_entities_in_df(self, test_project.get_trace_entries(), trace_df)
        TestAssertions.verify_entities_in_df(self, test_project.get_layer_mapping_entries(), layer_mapping_df)

    @staticmethod
    def generate_artifact_entries(artifact_ids: List[int], prefix: str = "None") -> List[Dict]:
        """
        Generates artifact for each index with given prefix.
        :param artifact_ids: The artifact ids to create artifacts for.
        :param prefix: The prefix to use before the artifact index in the artifact id.
        :return: List of artifact entries.
        """
        return [{
            "id": f"{prefix}{i}",
            "content": f"{prefix}_token{i}"
        } for i in artifact_ids]
