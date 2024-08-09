from abc import ABC, abstractmethod
from typing import Dict, Generic, Optional, Tuple, Type, TypeVar

from common_resources.tools.constants.symbol_constants import EMPTY_STRING
from common_resources.tools.util.base_object import BaseObject
from common_resources.tools.util.file_util import FileUtil
from common_resources.tools.util.override import overrides
from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.dataframes.layer_dataframe import LayerDataFrame
from common_resources.data.dataframes.trace_dataframe import TraceDataFrame
from common_resources.data.summarizer.artifacts_summarizer import ArtifactsSummarizer

ProjectData = TypeVar("ProjectData")
TraceDataFramesTypes = Tuple[ArtifactDataFrame, TraceDataFrame, LayerDataFrame]


class AbstractProjectReader(BaseObject, ABC, Generic[ProjectData]):
    """
    Defines interface for objects responsible for reading projects.
    """

    def __init__(self, overrides: dict = None, project_path: str = EMPTY_STRING):
        """
        Initialized project reader with overrides.
        :param overrides: The overrides to apply to project creator.
        :param project_path: Path to directory containing project data.
        """
        self.project_path = project_path
        self.project_path = project_path
        self.overrides = overrides if overrides else {}
        self.summarizer: Optional[ArtifactsSummarizer] = None

    def get_full_project_path(self) -> str:
        """
        Gets the project path for the reader
        :return: the project path
        """
        if self.project_path:
            return FileUtil.expand_paths(self.project_path)
        return self.project_path

    @abstractmethod
    def read_project(self) -> ProjectData:
        """
        Reads project data from files.
        :return: Returns data frames containing project data
        """

    @abstractmethod
    def get_project_name(self) -> str:
        """
        :return:  Returns the name of the project being read.
        """

    @staticmethod
    def should_generate_negative_links() -> bool:
        """
        :return: Returns whether negative links should be implied by comparing artifacts.
        """
        return True

    def get_overrides(self) -> Dict:
        """
        Returns any properties that should be overriden. This is a commonly used to set rules like
        allowing missing source / target references in trace links.
        :return: Dictionary of parameter names to their new values to override.
        """
        return self.overrides

    def set_summarizer(self, summarizer: ArtifactsSummarizer):
        """
        Sets the summarizer used to summarize content read by the reader
        :param summarizer: The summarizer to use
        :return: None
        """
        self.summarizer = summarizer

    @classmethod
    @overrides(BaseObject)
    def _get_enum_class(cls, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
        :param child_class_name: the name of the child class
        :return: the enum class mapping name to class
        """
        from common_resources.data.readers.supported_dataset_reader import SupportedDatasetReader
        return SupportedDatasetReader
