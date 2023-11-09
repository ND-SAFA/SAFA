import os
from datetime import datetime
from typing import Any, Type

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.util.file_util import FileUtil
from tgen.common.logging.logger_manager import logger
from tgen.data.exporters.abstract_dataset_exporter import AbstractDatasetExporter
from tgen.data.exporters.csv_exporter import CSVExporter
from tgen.data.exporters.dataframe_exporter import DataFrameExporter
from tgen.data.exporters.prompt_dataset_exporter import PromptDatasetExporter
from tgen.data.tdatasets.idataset import iDataset
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
import pandas as pd


class PipelineUtil:

    @staticmethod
    def save_dataset_checkpoint(dataset: Any, export_path: str = None,
                                filename: str = None, exporter_class: Type[AbstractDatasetExporter] = None) -> str:
        """
        Exports the dataset in the appropriate format
        :param dataset: The dataset to export
        :param export_path: The base path to export to
        :param filename: Name of the file to use when saving the dataset
        :param exporter_class: Exporter class to specify if not using defaults
        :return: The full export path
        """
        if not export_path:
            return EMPTY_STRING
        FileUtil.create_dir_safely(export_path)
        current_time_string = datetime.now().time().strftime('%Y-%m-%d %H:%M:%S')
        filename = current_time_string if not filename else filename
        full_export_path = os.path.join(export_path, filename)
        if not isinstance(dataset, iDataset) and not isinstance(dataset, pd.DataFrame):
            full_export_path = FileUtil.add_ext(full_export_path, FileUtil.YAML_EXT)
            FileUtil.write_yaml(dataset, full_export_path)
        else:
            save_as_trace_dataset = isinstance(dataset, TraceDataset) \
                                    or (isinstance(dataset, PromptDataset) and dataset.trace_dataset is not None)
            if exporter_class is None:
                exporter_class = DataFrameExporter if save_as_trace_dataset else CSVExporter
            if issubclass(exporter_class, CSVExporter) or not save_as_trace_dataset:
                full_export_path = FileUtil.add_ext(full_export_path, FileUtil.CSV_EXT)
            if isinstance(dataset, PromptDataset):
                exporter = PromptDatasetExporter(export_path=full_export_path, trace_dataset_exporter_type=exporter_class,
                                                 dataset=dataset)
            else:
                exporter = exporter_class(export_path=full_export_path, dataset=dataset)
            exporter.export()
        logger.info(f"Dataset checkpoint saved to {full_export_path} ")
        return full_export_path
