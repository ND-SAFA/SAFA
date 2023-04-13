from tgen.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.prompt_dataframe import PromptDataFrame
from tgen.data.readers.abstract_project_reader import AbstractProjectReader
from tgen.data.summarizer.summarizer import Summarizer
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.util.file_util import FileUtil


class PromptDatasetCreator(AbstractDatasetCreator[PromptDataset]):
    """
    Responsible for creating TraceDataset from DataFrames containing artifacts, traces, and
    layer mappings.
    """

    def __init__(self, project_reader: AbstractProjectReader = None, trace_dataset_creator: TraceDatasetCreator = None,
                 data_export_path: str = None, project_file_id: str = None, summarizer: Summarizer = None):
        """
        Initializes creator with entities extracted from reader.
        :param data_export_path: The path to where data files will be saved if specified.May be to a directory or specific file
        :param project_reader: Project reader responsible for extracting project entities.
        :param trace_dataset_creator: Data Creator responsible for making the trace dataset
        """
        super().__init__()
        self.data_export_path = data_export_path
        self.project_reader = project_reader
        self.trace_dataset_creator = trace_dataset_creator
        self.project_file_id = project_file_id
        if summarizer is not None:
            self._set_summarizer(summarizer)

    def create(self) -> PromptDataset:
        """
        Creates TraceDataset with links.
        :return: TraceDataset.
        """
        df = self.project_reader.read_project() if self.project_reader else None
        artifact_df = df if isinstance(df, ArtifactDataFrame) else None
        prompt_df = df if isinstance(df, PromptDataFrame) else None
        trace_dataset = self.trace_dataset_creator.create() if self.trace_dataset_creator else None
        return PromptDataset(prompt_df=prompt_df, artifact_df=artifact_df, trace_dataset=trace_dataset,
                             project_file_id=self.project_file_id, data_export_path=self.data_export_path)

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
        return ''

    def _set_summarizer(self, summarizer: Summarizer) -> None:
        """
        Sets summarizers for project readers
        :param summarizer: The summarizer to use
        :return: None
        """
        if self.project_reader is not None:
            self.project_reader.set_summarizer(summarizer)
        if self.trace_dataset_creator is not None:
            self.trace_dataset_creator.project_reader.set_summarizer(summarizer)
