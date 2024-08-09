import os
from abc import abstractmethod
from typing import Type

from common_resources.tools.util.base_object import BaseObject
from common_resources.tools.util.file_util import FileUtil
from common_resources.tools.util.override import overrides
from common_resources.data.creators.trace_dataset_creator import TraceDatasetCreator
from common_resources.data.tdatasets.idataset import iDataset
from common_resources.data.tdatasets.trace_dataset import TraceDataset


class AbstractDatasetExporter(BaseObject):

    def __init__(self, export_path: str, dataset_creator: TraceDatasetCreator = None, dataset: TraceDataset = None):
        """
        Responsible for exporting datasets
        :param export_path: Path to export project to.
        :param dataset_creator: The creator in charge of making the dataset to export
        :param dataset: The dataset to export if creator is not supplied
        """
        assert dataset_creator is not None or dataset is not None, f"Expected a dataset creator or a dataset but got {dataset}."
        self.dataset_creator = dataset_creator
        self._dataset = dataset
        self.export_path = self.update_export_path(export_path) if export_path else export_path

    def update_export_path(self, export_path: str) -> str:
        """
        Updates the path to export to
        :param export_path: New path to export to
        :return: Export path
        """
        self.export_path = FileUtil.expand_paths(export_path)
        export_path = FileUtil.get_directory_path(self.export_path)
        os.makedirs(export_path, exist_ok=True)
        return self.export_path

    def get_dataset(self) -> iDataset:
        """
        Gets the dataset to export
        :return: The dataset
        """
        if self._dataset is None:
            self._dataset = self.dataset_creator.create()
        return self._dataset

    @classmethod
    @overrides(BaseObject)
    def _get_enum_class(cls, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
        :param child_class_name: the name of the child class
        :return: the enum class mapping name to class
        """
        from common_resources.data.exporters.supported_dataset_exporters import SupportedDatasetExporter
        return SupportedDatasetExporter

    @staticmethod
    @abstractmethod
    def include_filename() -> bool:
        """
        Returns True if the dataset exporter expects the export path to include the filename, else False
        :return: True if the dataset exporter expects the export path to include the filename, else False
        """

    @abstractmethod
    def export(self, **kwargs):
        """
        Exports entities as a project in the appropriate format.
        :return: None
        """

    @classmethod
    def make_new(cls, export_path: str, dataset_creator: TraceDatasetCreator = None, dataset: TraceDataset = None) -> \
            "AbstractDatasetExporter":
        """
        Initializes a new class instance
        :param export_path: Path to export project to.
        :param dataset_creator: The creator in charge of making the dataset to export
        :param dataset: The dataset to export if creator is not supplied
        :return: A new dataset exporter of same type
        """
        return cls(export_path=export_path, dataset_creator=dataset_creator, dataset=dataset)
