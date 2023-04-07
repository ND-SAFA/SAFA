from abc import ABC, abstractmethod
from typing import Dict, Type, TypeVar, Generic, Tuple

from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.util.base_object import BaseObject
from tgen.util.override import overrides

PROJECT_DATA = TypeVar("PROJECT_DATA")
TraceDataFramesTypes = Tuple[ArtifactDataFrame, TraceDataFrame, LayerDataFrame]


class AbstractProjectReader(BaseObject, ABC, Generic[PROJECT_DATA]):
    """
    Defines interface for objects responsible for reading projects.
    """

    def __init__(self, overrides: dict = None):
        """
        Initialized project reader with overrides.
        :param overrides: The overrides to apply to project creator.
        """
        self.overrides = overrides if overrides else {}

    @abstractmethod
    def read_project(self) -> PROJECT_DATA:
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

    @classmethod
    @overrides(BaseObject)
    def _get_enum_class(cls, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
        :param child_class_name: the name of the child class
        :return: the enum class mapping name to class
        """
        from tgen.data.readers.supported_dataset_reader import SupportedDatasetReader
        return SupportedDatasetReader
