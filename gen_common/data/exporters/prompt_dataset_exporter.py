import os
from typing import Type, Union

from gen_common.constants import ARTIFACT_FILE_NAME, PROJECT_SUMMARY_FILENAME
from gen_common.data.creators.prompt_dataset_creator import PromptDatasetCreator
from gen_common.data.exporters.abstract_dataset_exporter import AbstractDatasetExporter
from gen_common.data.exporters.supported_dataset_exporters import SupportedDatasetExporter
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.util import FileUtil


class PromptDatasetExporter(AbstractDatasetExporter):

    def __init__(self, export_path: str,
                 trace_dataset_exporter_type: Union[
                     SupportedDatasetExporter, Type[AbstractDatasetExporter]] = SupportedDatasetExporter.DF,
                 dataset_creator: PromptDatasetCreator = None, dataset: PromptDataset = None):
        """
        Initializes the dataset to export the given dataset to the export path in the format provided
        :param export_path: The path to export the dataset to
        :param trace_dataset_exporter_type: The type of exporter to use to save the trace dataset (if applicable)
        :param dataset_creator: The creator to make the dataset to export
        :param dataset: The dataset to export
        """
        super().__init__(export_path=export_path, dataset_creator=dataset_creator, dataset=dataset)
        self.trace_dataset_exporter_type = trace_dataset_exporter_type.value if isinstance(
            trace_dataset_exporter_type, SupportedDatasetExporter) else trace_dataset_exporter_type

    @staticmethod
    def include_filename() -> bool:
        """
       Returns False bc the dataset exporter does not expect the export path to include the filename
       :return: False
       """
        return False

    def export(self, **kwargs) -> None:
        """
        Exports the prompt dataset
        :param kwargs: Any additional parameters to give to the trace dataset exporter
        :return: None
        """
        dataset: PromptDataset = self.get_dataset()
        if dataset.project_summary:
            project_summary_path = os.path.join(FileUtil.get_directory_path(self.export_path), PROJECT_SUMMARY_FILENAME)
            dataset.project_summary.save(FileUtil.add_ext(project_summary_path, FileUtil.TEXT_EXT))
            dataset.project_summary.save(FileUtil.add_ext(project_summary_path, FileUtil.JSON_EXT))
        if dataset.trace_dataset is not None:
            exporter: AbstractDatasetExporter = self.trace_dataset_exporter_type(export_path=self.export_path,
                                                                                 dataset=dataset.trace_dataset)
            exporter.export(**kwargs)
        elif dataset.artifact_df is not None:
            export_path = self.export_path if FileUtil.is_file(self.export_path) \
                else os.path.join(self.export_path, ARTIFACT_FILE_NAME)
            dataset.artifact_df.to_csv(export_path)
        elif dataset.prompt_df is not None:
            dataset.export_prompt_dataframe(dataset.prompt_df, self.export_path)
