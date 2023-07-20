from typing import Dict, List, Tuple

from tgen.common.artifact import Artifact
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.data.readers.abstract_project_reader import AbstractProjectReader
from tgen.data.readers.api_project_reader import ApiProjectReader
from tgen.ranking.common.trace_layer import TraceLayer
from tgen.testres.test_data_manager import TestDataManager
from tgen.testres.testprojects.abstract_test_project import AbstractTestProject
from tgen.testres.testprojects.entry_creator import EntryCreator, LayerEntry, TraceInstruction
from tgen.util.override import overrides


class ApiTestProject(AbstractTestProject):
    """
    Contains entries for classic trace project.
    """

    @staticmethod
    def get_project_path() -> str:
        """
        :return: Throws eror because api project does not have path.
        """
        raise ValueError("Classic trace does not contain project path.")

    @classmethod
    def get_project_reader(cls) -> AbstractProjectReader:
        """
        :return: Returns project reader with project data as api payload
        """
        return TestDataManager.get_project_reader()

    @staticmethod
    def get_n_links() -> int:
        """
        :return: Returns the number of links after t3 and s6 are removed.
        """
        return 18  # t3 and s6 are removed

    @classmethod
    def get_n_positive_links(cls) -> int:
        """
        :return: Returns number of positive links defined for project
        """
        return len(TestDataManager.DATA[TestDataManager.Keys.TRACES])

    @staticmethod
    @overrides(AbstractTestProject)
    def get_source_entries() -> List[Artifact]:
        """
        :return: Returns entries for source artifacts for layer 1 and 2 and test data manager.
        """
        return EntryCreator.get_entries_in_type(TestDataManager.Keys.SOURCE)

    @staticmethod
    @overrides(AbstractTestProject)
    def get_target_entries() -> List[LayerEntry]:
        """
        :return: Returns entries for target artifacts for layer 1 and 2 and test data manager.
        """
        return EntryCreator.get_entries_in_type(TestDataManager.Keys.TARGET)

    @classmethod
    def get_trace_entries(cls) -> List[Dict]:
        """
        :return: Returns entries for positive trace links defined in project.
        """
        trace_data: List[Dict] = TestDataManager.DATA[TestDataManager.Keys.TRACES]
        trace_data: List[TraceInstruction] = [(t["source"], t["target"], t["label"]) for t in trace_data]
        return EntryCreator.create_trace_entries(trace_data)

    @classmethod
    def get_layer_mapping_entries(cls) -> List[TraceLayer]:
        """
        :return: Returns entries for layer mappings between two layers.
        """
        layer_mapping_data = [
            (
                ApiProjectReader.create_layer_id(StructuredKeys.LayerMapping.SOURCE_TYPE.value, 0),
                ApiProjectReader.create_layer_id(StructuredKeys.LayerMapping.TARGET_TYPE.value, 0)
            ),
            (
                ApiProjectReader.create_layer_id(StructuredKeys.LayerMapping.SOURCE_TYPE.value, 1),
                ApiProjectReader.create_layer_id(StructuredKeys.LayerMapping.TARGET_TYPE.value, 1)
            )
        ]
        return EntryCreator.create_layer_mapping_entries(layer_mapping_data)

    @classmethod
    def get_expected_links(self) -> List[Tuple[str, str]]:
        """
        :return:Returns expected links between source and target artifacts.
        """
        artifact_layer_map = TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS])
        links = []

        for trace_layer in TestDataManager.get_path([TestDataManager.Keys.LAYERS]):
            parent_artifacts = artifact_layer_map[trace_layer["parent"]]
            child_artifacts = artifact_layer_map[trace_layer["child"]]

            for p_id, p_body in parent_artifacts.items():
                for c_id, c_body in child_artifacts.items():
                    links.append((c_id, p_id))

        return links

    @staticmethod
    def get_positive_links() -> List[Tuple[str, str]]:
        """
        :return: Returns positive trace link entries.
        """
        traces = [(t["source"], t["target"]) for t in TestDataManager.get_path(TestDataManager.Keys.TRACES)]
        return traces

    @staticmethod
    def get_negative_links() -> List[Tuple[str, str]]:
        """
        :return: Return negative trace link entries.
        """
        all_links = ApiTestProject.get_expected_links()
        pos_links = ApiTestProject.get_positive_links()
        return list(set(all_links).difference(set(pos_links)))

    @staticmethod
    def get_positive_link_ids() -> List[int]:
        """
        :return: Returns the link of ids of the positive links.
        """
        positive_links = ApiTestProject.get_positive_links()
        return ApiTestProject._get_link_ids(positive_links)

    @staticmethod
    def _get_link_ids(links_list: List[Tuple[str, str]]) -> List[int]:
        """
        Returns the ids of the link entries.
        :param links_list: Link entries containing tuples between source id and target id.
        :return: List of ids.
        """
        return list(TestDataManager.create_trace_dataframe(links_list).index)
