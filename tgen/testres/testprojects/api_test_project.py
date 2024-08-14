from typing import List, Tuple

from common_resources.data.readers.abstract_project_reader import AbstractProjectReader
from tgen.testres.test_data_manager import TestDataManager
from tgen.testres.testprojects.abstract_test_project import AbstractTestProject


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
