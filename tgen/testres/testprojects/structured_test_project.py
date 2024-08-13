from typing import Dict, List

from common_resources.data.readers.abstract_project_reader import AbstractProjectReader
from common_resources.data.readers.structured_project_reader import StructuredProjectReader

from tgen.common.objects.trace_layer import TraceLayer
from tgen.testres.paths.project_paths import STRUCTURE_PROJECT_PATH
from tgen.testres.testprojects.abstract_test_project import AbstractTestProject
from tgen.testres.testprojects.entry_creator import EntryCreator


class StructuredTestProject(AbstractTestProject):
    """
    Defines testing expectations for structured project.
    """

    @staticmethod
    def get_project_path() -> str:
        """
        :return: Returns path to structured project.
        """
        return STRUCTURE_PROJECT_PATH

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
