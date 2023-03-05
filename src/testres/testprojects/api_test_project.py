from typing import Dict, List, Tuple

from data.keys.structure_keys import StructuredKeys
from data.readers.abstract_project_reader import AbstractProjectReader
from data.readers.api_project_reader import ApiProjectReader
from testres.test_data_manager import TestDataManager
from testres.testprojects.abstract_test_project import AbstractTestProject
from testres.testprojects.entry_creator import EntryCreator, LayerEntry, TraceInstruction
from util.override import overrides


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
        data = {
            "source_layers": TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.SOURCE]),
            "target_layers": TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.TARGET]),
            "true_links": TestDataManager.get_path(TestDataManager.Keys.TRACES)
        }
        return ApiProjectReader(data)

    @staticmethod
    def get_n_links() -> int:
        """
        :return: Returns the number of links after t3 and s6 are removed.
        """
        return 12  # t3 and s6 are removed

    @classmethod
    def get_n_positive_links(cls) -> int:
        """
        :return: Returns number of positive links defined for project
        """
        return len(TestDataManager.DATA[TestDataManager.Keys.TRACES])

    @staticmethod
    @overrides(AbstractTestProject)
    def get_source_entries() -> List[LayerEntry]:
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
        trace_data = TestDataManager.DATA[TestDataManager.Keys.TRACES]
        trace_data: List[TraceInstruction] = [(a_id, a_body, 1) for a_id, a_body in trace_data]
        return EntryCreator.create_trace_entries(trace_data)

    @classmethod
    def get_layer_mapping_entries(cls) -> List[Dict]:
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
        sources = TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.SOURCE])
        targets = TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.TARGET])
        links = []
        for source_dict, target_dict in zip(sources, targets):
            for source_id, source_body in source_dict.items():
                for target_id, target_body in target_dict.items():
                    links.append((source_id, target_id))
        return links

    @staticmethod
    def get_positive_links():
        """
        :return: Returns positive trace link entries.
        """
        return TestDataManager.get_path(TestDataManager.Keys.TRACES)

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
        return list(TestDataManager.create_trace_dataframe(links_list).keys())
