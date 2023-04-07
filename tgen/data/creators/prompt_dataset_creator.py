from collections import Counter
from typing import Any, Dict, List, Set

import pandas as pd

from tgen.constants import ALLOWED_MISSING_SOURCES_DEFAULT, ALLOWED_MISSING_TARGETS_DEFAULT, ALLOWED_ORPHANS_DEFAULT, \
    NO_ORPHAN_CHECK_VALUE, REMOVE_ORPHANS_DEFAULT
from tgen.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.prompt_dataframe import PromptDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.data.processing.cleaning.data_cleaner import DataCleaner
from tgen.data.prompts.abstract_prompt_generator import AbstractPromptGenerator
from tgen.data.prompts.classification_prompt_generator import ClassificationPromptGenerator
from tgen.data.readers.abstract_project_reader import AbstractProjectReader
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.util.dataframe_util import DataFrameUtil
from tgen.util.dict_util import ListUtil
from tgen.util.file_util import FileUtil
from tgen.util.logging.logger_manager import logger
from tgen.util.reflection_util import ReflectionUtil
from tgen.util.thread_util import ThreadUtil


class PromptDatasetCreator(AbstractDatasetCreator[PromptDataset]):
    """
    Responsible for creating TraceDataset from DataFrames containing artifacts, traces, and
    layer mappings.
    """

    def __init__(self, project_reader: AbstractProjectReader = None, trace_dataset_creator: TraceDatasetCreator = None,
                 data_output_path: str = None, project_file_id: str = None, ):
        """
        Initializes creator with entities extracted from reader.
        :param data_output_path: The path to where data files will be saved
        :param project_reader: Project reader responsible for extracting project entities.
        :param trace_dataset_creator: Data Creator responsible for making the trace dataset
        """
        super().__init__()
        self.data_output_path = data_output_path
        self.project_reader = project_reader
        self.trace_dataset_creator = trace_dataset_creator
        self.project_file_id = project_file_id

    def create(self) -> PromptDataset:
        """
        Creates TraceDataset with links.
        :return: TraceDataset.
        """
        trace_dataset = self.trace_dataset_creator.create() if self.trace_dataset_creator else None
        df = self.project_reader.read_project() if self.project_reader else None
        artifact_df = df if isinstance(df, ArtifactDataFrame) else None
        prompt_df = df if isinstance(df, PromptDataFrame) else None
        return PromptDataset(prompt_df=prompt_df, artifact_df=artifact_df, trace_dataset=trace_dataset,
                             project_file_id=self.project_file_id, data_output_path=self.data_output_path)

    def get_name(self) -> str:
        """
        Gets the name of the prompt dataset based on given params
        :return: The name of the prompt dataset
        """
        if self.project_reader:
            return self.project_reader.get_project_name()
        if self.data_output_path:
            return FileUtil.get_file_name(self.data_output_path)
        if self.project_file_id:
            return self.project_file_id
        return ''
