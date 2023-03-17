import os
from abc import abstractmethod

from typing import Type

from data.creators.supported_dataset_creator import SupportedDatasetCreator
from data.creators.trace_dataset_creator import TraceDatasetCreator
from data.datasets.trace_dataset import TraceDataset
from util.base_object import BaseObject
from util.override import overrides


class AbstractDatasetExporter(BaseObject):

    def __init__(self, export_path: str, dataset_creator: TraceDatasetCreator = None, dataset: TraceDataset = None):
        """
        Responsible for exporting datasets
        :param export_path: Path to export project to.
        :param dataset_creator: The creator in charge of making the dataset to export
        """
        assert dataset_creator is not None or dataset is not None, "Must supply either a dataset creator or a dataset"
        self.dataset_creator = dataset_creator
        self.export_path = export_path
        self.dataset = dataset
        os.makedirs(self.export_path, exist_ok=True)

    def get_dataset(self) -> TraceDataset:
        """
        Gets the dataset to export
        :return: The dataset
        """
        if self.dataset is None:
            self.dataset = self.dataset_creator.create()
        return self.dataset

    @abstractmethod
    def export(self):
        """
        Exports entities as a project in the appropriate format.
        :return: None
        """

    @classmethod
    @overrides(BaseObject)
    def _get_child_enum_class(cls, abstract_class: Type, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
        :param abstract_class: the abstract parent class type
        :param child_class_name: the name of the child class
        :return: the enum class mapping name to class
        """
        return SupportedDatasetCreator
