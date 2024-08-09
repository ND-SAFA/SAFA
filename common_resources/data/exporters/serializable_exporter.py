import json
from typing import Dict, List, Any

from common_resources.data.creators.prompt_dataset_creator import PromptDatasetCreator
from common_resources.data.dataframes.abstract_project_dataframe import AbstractProjectDataFrame
from common_resources.data.exporters.abstract_dataset_exporter import AbstractDatasetExporter
from common_resources.data.summarizer.summary import Summary
from common_resources.data.tdatasets.idataset import iDataset
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.data.tdatasets.trace_dataset import TraceDataset
from common_resources.tools.constants.symbol_constants import EMPTY_STRING, UNDERSCORE
from common_resources.tools.util.json_util import JsonUtil


class SerializableExporter(AbstractDatasetExporter):

    def __init__(self, dataset_creator: PromptDatasetCreator = None, dataset: PromptDataset = None, export_path: str = EMPTY_STRING):
        """
        Initializes exporter for given trace dataset.
        :param dataset: The dataset to export
        :param dataset_creator: The creator in charge of making the dataset to export
        :param export_path: The path to export the dataset to
        """
        super().__init__(dataset_creator=dataset_creator, dataset=dataset, export_path=export_path)

    def export(self, **kwargs) -> Dict[str, Dict | str | List]:
        """
        Exports the dataset to the ApiDefinition format
        :return: The ApiDefinition
        """
        dataset: PromptDataset = self.get_dataset()
        output = self._dataset_to_json_serializable(dataset)

        if self.export_path:
            JsonUtil.save_to_json_file(output, self.export_path)

        return output

    @staticmethod
    def include_filename() -> bool:
        """
        Returns True bc the dataset exporter expects the export path to include the filename
        :return: True
        """
        return True

    @staticmethod
    def _dataset_to_json_serializable(dataset: iDataset) -> Dict[str, Dict | str | List]:
        """
        Converts a dataset to JSON by converting all fields and including in a dictionary.
        :param dataset: The dataset to convert.
        :return: Dictionary mapping param name to the converted value.
        """
        output = {}
        for name, value in vars(dataset).items():
            if name.startswith(UNDERSCORE) or value is None:
                continue
            if isinstance(value, TraceDataset):
                output[name] = SerializableExporter._dataset_to_json_serializable(value)
            elif isinstance(value, AbstractProjectDataFrame):
                output[name] = value.to_dict(orient='list', index=value.index_name() is not None)
            elif isinstance(value, Summary):
                output[name] = value.to_string()
            else:
                converted = SerializableExporter._obj_to_json_serializable(value)
                if converted is not None:
                    output[name] = converted
        return output

    @staticmethod
    def _obj_to_json_serializable(obj: Any) -> Any:
        """
        Converts an object to JSON if natively serializable, otherwise returns None.
        :param obj: The object to convert.
        :return: The serializable obj.
        """
        try:
            return json.dumps(obj)
        except (TypeError, OverflowError):
            return None
