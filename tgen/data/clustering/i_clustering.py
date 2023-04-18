from abc import abstractmethod, ABC
from typing import Dict, Any, Type
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.util.base_object import BaseObject
from tgen.util.override import overrides

Clusters = Dict[Any, str]


class iClusteringMethod(BaseObject, ABC):

    @staticmethod
    @abstractmethod
    def cluster(trace_dataset: TraceDataset) -> Clusters:
        """
        Creates clusters of artifacts in the dataset
        :return: A dictionary mapping artifact id to its cluster num
        """

    @classmethod
    @overrides(BaseObject)
    def _get_enum_class(cls, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
        :param child_class_name: the name of the child class
        :return: the enum class mapping name to class
        """
        from tgen.data.clustering.SupportedClusteringMethod import SupportedClusteringMethod
        return SupportedClusteringMethod
