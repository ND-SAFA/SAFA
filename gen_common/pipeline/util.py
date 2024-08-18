import os
from datetime import datetime
from functools import wraps
from typing import Any, Type

import pandas as pd

from gen_common.constants.symbol_constants import EMPTY_STRING, NEW_LINE
from gen_common.data.exporters.abstract_dataset_exporter import AbstractDatasetExporter
from gen_common.data.exporters.csv_exporter import CSVExporter
from gen_common.data.exporters.dataframe_exporter import DataFrameExporter
from gen_common.data.exporters.prompt_dataset_exporter import PromptDatasetExporter
from gen_common.data.tdatasets.idataset import iDataset
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.data.tdatasets.trace_dataset import TraceDataset
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.pipeline.abstract_pipeline_step import title_format_for_logs
from gen_common.pipeline.state import State
from gen_common.util.file_util import FileUtil
from gen_common.util.reflection_util import ReflectionUtil


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


def nested_pipeline(parent_pipeline_state: Type[State]) -> Any:
    """
    Decorator for using a different pipeline inside of a pipeline
    :param parent_pipeline_state: The state of the pipeline calling the nested pipeline
    :return: The result of the function
    """

    def decorator(func):
        """
        Logic for creating the decorator
        :param func: Function containing the nested pipeline call
        :return: Result of the function
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Handles running the function and any pre or post processing actions
            :param args: The arguments to the function
            :param kwargs: The kwargs to the function
            :return: The result of the function
            """
            result = None
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                parent_pipeline_name = ReflectionUtil.get_class_name(parent_pipeline_state)
                parent_pipeline_name = parent_pipeline_name.replace(ReflectionUtil.get_class_name(State), EMPTY_STRING)
                logger.log_with_title(f"Returning to {parent_pipeline_name}",
                                      formatting=NEW_LINE + title_format_for_logs)
            return result

        return wrapper

    return decorator
