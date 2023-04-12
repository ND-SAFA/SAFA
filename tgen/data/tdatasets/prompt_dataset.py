import os
import uuid
from typing import Any, Tuple

from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.prompt_dataframe import PromptDataFrame
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.prompts.abstract_prompt_generator import AbstractPromptGenerator
from tgen.data.prompts.classification_prompt_generator import ClassificationPromptGenerator
from tgen.data.readers.prompt_project_reader import PromptProjectReader
from tgen.data.tdatasets.idataset import iDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.models.model_manager import ModelManager
import openai

import pandas as pd

from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.dataframe_util import DataFrameUtil
from tgen.util.file_util import FileUtil


class PromptDataset(iDataset):
    """
    Represents a dataset for prompt-based (generative) models such as GPT
    """

    def __init__(self, prompt_df: PromptDataFrame = None, artifact_df: ArtifactDataFrame = None,
                 trace_dataset: TraceDataset = None, project_file_id: str = None, data_export_path: str = None):
        """
        Initializes the dataset with necessary artifact/trace information and generator for the prompts
        :param prompt_df: The prompt dataframe
        :param artifact_df: The dataframe containing project artifacts
        :param trace_dataset: The dataset containing trace links and artifacts
        :param project_file_id: The file id used by open AI
        :param data_export_path: The path to where data files will be saved if specified. May be to a directory or specific file
        """
        self.prompt_df = prompt_df
        self.artifact_df = artifact_df
        self.trace_dataset = trace_dataset
        self.project_file_id = project_file_id
        self.data_export_path = data_export_path
        if not self.project_file_id and prompt_df is None:
            assert self._has_trace_data(), "Either artifacts dataframe or trace dataframe must be provided to generate dataset."

    def to_hf_dataset(self, model_generator: ModelManager) -> Any:
        """
        Converts data to a Huggingface (HF) Dataset.
        :param model_generator: The model generator determining architecture and feature function for trace links.
        :return: A data in a HF Dataset.
        """
        raise NotImplementedError("A prompt dataset for hugging face is currently not supported")

    def to_trainer_dataset(self, prompts_generator: AbstractPromptGenerator) -> pd.DataFrame:
        """
        Converts data to that used by Huggingface (HF) trainer.
        :param prompts_generator: The model generator determining architecture and feature function for trace links.
        :return: A data used by the HF trainer.
        """
        return self.get_prompts_dataframe(prompts_generator)

    def export_prompt_dataset(self, prompt_df: pd.DataFrame, export_path: str = None) -> Tuple[str, bool]:
        """
        Exports the prompt dataset
        :param prompt_df: The dataframe containing prompts and completions
        :param export_path: Path to save the prompt dataset to
        :return: The path to the dataset and whether it should be deleted after being used
        """
        export_path = export_path if export_path else self.data_export_path
        should_delete = not export_path
        default_filename = f"{uuid.uuid4()}{PromptProjectReader.FILE_EXT}"
        if export_path:
            if not FileUtil.get_file_ext(export_path):
                export_path = os.path.join(export_path, default_filename)
            FileUtil.create_dir_safely(os.path.dirname(export_path))
        else:
            export_path = os.path.join(os.getcwd(), default_filename)
        prompt_df.to_json(export_path, orient='records', lines=True)
        return export_path, should_delete

    def get_project_file_id(self, prompt_generator: AbstractPromptGenerator = None) -> str:
        """
        Gets the project file id used by open_ai
        :param prompt_generator: The generator of prompts for the dataset
        :return: The project file id used by open_ai
        """
        if not self.project_file_id:
            export_path, should_delete_path = self.export_prompt_dataset(self.get_prompts_dataframe(prompt_generator))
            res = openai.File.create(file=open(export_path), purpose=TrainerTask.TRAIN.value)
            self.project_file_id = res.id
            if should_delete_path:
                os.remove(export_path)
        return self.project_file_id

    def get_prompts_dataframe(self, prompt_generator: AbstractPromptGenerator = None) -> pd.DataFrame:
        """
        Gets the prompt dataframe containing prompts and completions
        :param prompt_generator: The generator of prompts for the dataset
        :return: The prompt dataframe containing prompts and completions
        """
        if self.prompt_df is None:
            assert prompt_generator is not None, "Must provide prompt generator to create prompt dataset for trainer"
            assert self._has_trace_data(), "Either artifacts dataframe or trace dataframe to generate dataframe."
            self.prompt_df = self._generate_prompts_dataframe_from_traces(prompt_generator) if self.trace_dataset \
                else self._generate_prompts_dataframe_from_artifacts(prompt_generator)
        return self.prompt_df

    def _generate_prompts_dataframe_from_traces(self, prompt_generator: AbstractPromptGenerator) -> pd.DataFrame:
        """
        Converts trace links in to prompt format for generation model.
        :param prompt_generator: The generator of prompts for the dataset
        :return: A prompts based dataset.
        """
        entries = []
        traces = self.trace_dataset.trace_df if isinstance(prompt_generator, ClassificationPromptGenerator) \
            else DataFrameUtil.query_df(self.trace_dataset.trace_df, {TraceKeys.LABEL.value: 1})
        for i, row in traces.iterrows():
            source, target = self.trace_dataset.get_link_source_target_artifact(link_id=i)
            entry = prompt_generator.generate(source[ArtifactKeys.CONTENT], target[ArtifactKeys.CONTENT],
                                              label=row[TraceKeys.LABEL.value])
            entries.append(entry)
        return pd.DataFrame(entries)

    def _generate_prompts_dataframe_from_artifacts(self, prompt_generator: AbstractPromptGenerator) -> pd.DataFrame:
        """
        Converts artifacts in to prompt format for generation model.
        :param prompt_generator: The generator of prompts for the dataset
        :return: A prompts based dataset.
        """
        entries = []
        for i, row in self.artifact_df.iterrows():
            entry = prompt_generator.generate(target_content=row[ArtifactKeys.CONTENT.value], source_content='')
            entries.append(entry)
        return pd.DataFrame(entries)

    def _has_trace_data(self) -> bool:
        """
        Returns True when project data in the form of an artifacts_df or trace_dataset has been provided, else False
        :return: True when project data in the form of an artifacts_df or trace_dataset has been provided, else False
        """
        return not (self.artifact_df is None and self.trace_dataset is None)
