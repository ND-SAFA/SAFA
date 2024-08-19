from typing import Dict, List

from gen_common.data.objects.trace_layer import TraceLayer
from gen_common.data.readers.abstract_project_reader import AbstractProjectReader
from gen_common.data.readers.structured_project_reader import StructuredProjectReader
from gen_common_test.base.paths.project_paths import GEN_COMMON_TEST_PROJECT_STRUCTURE_PATH
from gen_common_test.testprojects.abstract_test_project import AbstractTestProject
from gen_common_test.testprojects.entry_creator import EntryCreator


class StructuredTestProject(AbstractTestProject):
    """
    Defines testing expectations for structured project.
    """

    @staticmethod
    def get_project_path() -> str:
        """
        :return: Returns path to structured project.
        """
        return GEN_COMMON_TEST_PROJECT_STRUCTURE_PATH

    @classmethod
    def get_project_reader(cls) -> AbstractProjectReader:
        """
        :return: Returns reader to structured project.
        """
        return StructuredProjectReader(cls.get_project_path())

    @staticmethod
    def get_n_links() -> int:
        """
        :return: Returns the number of expected links betwen 2 source and 4 targerts.
        """
        return 8

    @classmethod
    def get_n_positive_links(cls) -> int:
        """
        :return: Returns the number of positive links in project.
        """
        return 4

    @classmethod
    def get_trace_entries(cls) -> List[Dict]:
        """
        :return: Return trace entries of positive links defined in project.
        """
        trace_data = [(1674, 80), (1674, 85), (1688, 142), (1688, 205)]
        return EntryCreator.create_trace_entries(trace_data)

    @classmethod
    def get_trace_layers(cls) -> List[TraceLayer]:
        """
        :return: Returns the layer mapping entries in project between source and target.
        """
        return [TraceLayer(child="Requirements", parent="Regulatory Codes")]
