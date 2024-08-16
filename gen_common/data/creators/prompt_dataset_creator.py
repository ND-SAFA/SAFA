import os
from typing import Optional, Union

from gen_common.constants import EMPTY_STRING, PROJECT_SUMMARY_FILENAME
from gen_common.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from gen_common.data.creators.trace_dataset_creator import TraceDatasetCreator
from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.dataframes.prompt_dataframe import PromptDataFrame
from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.data.readers.abstract_project_reader import AbstractProjectReader
from gen_common.data.readers.artifact_project_reader import ArtifactProjectReader
from gen_common.data.summarizer.artifacts_summarizer import ArtifactsSummarizer
from gen_common.data.summarizer.summary import Summary
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.util import FileUtil


class PromptDatasetCreator(AbstractDatasetCreator[PromptDataset]):
    """
    Responsible for creating TraceDataset from DataFrames containing artifacts, traces, and
    layer mappings.
    """

    def __init__(self, project_reader: AbstractProjectReader = None, trace_dataset_creator: TraceDatasetCreator = None,
                 data_export_path: str = None, project_file_id: str = None, project_summary: Union[Summary, str] = None,
                 summarizer: ArtifactsSummarizer = None, ensure_code_is_summarized: bool = False):
        """
        Initializes creator with entities extracted from reader.
        :param project_reader: Project reader responsible for extracting project entities.
        :param trace_dataset_creator: Data Creator responsible for making the trace dataset
        :param data_export_path: The path to where data files will be saved if specified.May be to a directory or specific file
        :param project_file_id: File used to load prompt dataset.
        :param project_summary: Default project summary.
        :param summarizer: Summarizer used to summarize artifact content.
        :param ensure_code_is_summarized: Verifies that code is summarized and summarizes code that's not.
        """
        super().__init__()
        self.project_reader = project_reader
        self.trace_dataset_creator = trace_dataset_creator
        self.project_file_id = project_file_id
        self.ensure_code_is_summarized = ensure_code_is_summarized
        self.summarizer = summarizer
        self.project_summary = project_summary
        if self.summarizer is not None:
            self.set_summarizers(summarizer)
        self.data_export_path = data_export_path

    def create(self) -> PromptDataset:
        """
        Creates TraceDataset with links.
        :return: TraceDataset.
        """
        df = self.project_reader.read_project() if self.project_reader else None
        artifact_df = df if isinstance(df, ArtifactDataFrame) else None
        prompt_df = df if isinstance(df, PromptDataFrame) else None
        trace_dataset = self.trace_dataset_creator.create() if self.trace_dataset_creator else None
        project_summary = self.__load_project_summary()
        dataset = PromptDataset(prompt_df=prompt_df, artifact_df=artifact_df, trace_dataset=trace_dataset,
                                project_file_id=self.project_file_id, data_export_path=self.data_export_path,
                                project_summary=project_summary)
        if self.ensure_code_is_summarized:
            dataset = self._conditionally_summarize_dataset(dataset)
        return dataset

    def _conditionally_summarize_dataset(self, dataset: PromptDataset) -> PromptDataset:
        """
        Summarizes any code files that are not summarized
        :param dataset: The original dataset (possible without summaries)
        :return: The summarized dataset
        """
        if dataset.artifact_df is not None and not dataset.artifact_df.is_summarized(code_or_above_limit_only=True):
            summarizer = ArtifactsSummarizer(summarize_code_only=True,
                                             project_summary=dataset.project_summary)
            dataset.artifact_df.summarize_content(summarizer)  # summarize any artifacts that were not in existing summaries
        return dataset

    def _use_existing_summaries(self, dataset: PromptDataset, summary_path: str) -> None:
        """
        Updates the dataset with any existing summaries
        :param dataset: The dataset being summarized
        :param summary_path: The path to the existing summaries
        :return: None (updates directly)
        """
        artifact_df = ArtifactProjectReader(project_path=summary_path).read_project()
        artifact_df = artifact_df.filter_by_index(dataset.artifact_df.index)
        dataset.artifact_df.update_values(ArtifactKeys.SUMMARY, artifact_df.index, artifact_df[ArtifactKeys.SUMMARY])
        if not dataset.project_summary:
            dataset.project_summary = self.read_project_summary(summary_path)

    @staticmethod
    def read_project_summary(project_path: str) -> Optional[Summary]:
        """
        Reads the project summary if it exists
        :param project_path: Path to directory containing project data.
        :return: The project summary
        """
        project_dir = FileUtil.get_directory_path(project_path)
        for filename_ext in [FileUtil.JSON_EXT, FileUtil.TEXT_EXT]:
            filename = FileUtil.add_ext(PROJECT_SUMMARY_FILENAME, filename_ext)
            project_summary_path = os.path.join(project_dir, filename)
            if os.path.exists(project_summary_path):
                return Summary.load_from_file(project_summary_path)
        return None

    def get_project_path(self) -> str:
        """
        Returns the project path from the reader or creator if provided
        :return: The project path
        """
        project_reader = self.trace_dataset_creator.project_reader if self.trace_dataset_creator else self.project_reader
        project_path = project_reader.get_full_project_path() if project_reader else EMPTY_STRING
        return project_path

    def get_name(self) -> str:
        """
        Gets the name of the prompt dataset based on given params
        :return: The name of the prompt dataset
        """
        if self.project_reader:
            return self.project_reader.get_project_name()
        if self.data_export_path:
            return FileUtil.get_file_name(self.data_export_path)
        if self.project_file_id:
            return self.project_file_id
        return EMPTY_STRING

    def set_summarizers(self, summarizer: ArtifactsSummarizer) -> None:
        """
        Sets summarizers for project readers
        :param summarizer: The summarizer to use
        :return: None
        """
        self.summarizer = summarizer
        if self.project_reader is not None:
            self.project_reader.set_summarizer(summarizer)
        if self.trace_dataset_creator is not None:
            self.trace_dataset_creator.project_reader.set_summarizer(summarizer)

    def __load_project_summary(self) -> Summary:
        """
        Loads project summary from either the summary object, a string, or the project path.
        :return: Initialized summary object.
        """
        if isinstance(self.project_summary, Summary):
            return self.project_summary
        elif isinstance(self.project_summary, str):
            return Summary.from_string(self.project_summary)
        else:
            return self.read_project_summary(self.get_project_path())
