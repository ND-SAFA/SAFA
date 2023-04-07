import os
from typing import Any

from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.prompt_dataframe import PromptDataFrame
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.prompts.abstract_prompt_generator import AbstractPromptGenerator
from tgen.data.prompts.classification_prompt_generator import ClassificationPromptGenerator
from tgen.data.tdatasets.idataset import iDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.models.model_manager import ModelManager
import openai

import pandas as pd

from tgen.train.open_ai.open_ai_task import OpenAITask
from tgen.util.file_util import FileUtil


class PromptDataset(iDataset):
    """
    Represents a dataset for prompt-based (generative) models such as GPT
    """

    def __init__(self, prompt_df: PromptDataFrame = None, artifact_df: ArtifactDataFrame = None,
                 trace_dataset: TraceDataset = None, project_file_id: str = None, data_output_path: str = None):
        """
        Initializes the dataset with necessary artifact/trace information and generator for the prompts
        :param prompt_df: The prompt dataframe
        :param artifact_df: The dataframe containing project artifacts
        :param trace_dataset: The dataset containing trace links and artifacts
        :param project_file_id: The file id used by open AI
        :param data_output_path: The path to export dataset to if needed
        """
        self.prompt_df = prompt_df
        self.artifact_df = artifact_df
        self.trace_dataset = trace_dataset
        self.project_file_id = project_file_id
        self.data_output_path = data_output_path
        if not self.project_file_id or not prompt_df:
            assert self.artifact_df or self.trace_dataset and self.data_output_path, "Must provide a data_file_output_path and " \
                                                                                      "either artifacts dataframe " \
                                                                                      "or trace dataframe to generate dataset."
            FileUtil.create_dir_safely(self.data_output_path)

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

    def export_prompt_dataset(self, prompt_df: pd.DataFrame) -> str:
        """
        Exports the prompt dataset
        :param prompt_df: The dataframe containing prompts and completions
        :return: The path to the dataset
        """
        prompt_df.to_json(self.data_output_path, orient='records', lines=True)
        return self.data_output_path

    def get_project_file_id(self) -> str:
        """
        Gets the project file id used by open_ai
        :return: The project file id used by open_ai
        """
        if not self.project_file_id:
            dataset_file_path = self.export_prompt_dataset(self.get_prompts_dataframe())
            res = openai.File.create(file=open(dataset_file_path), purpose=OpenAITask.FINE_TUNE.value)
            self.project_file_id = res.id
        return self.project_file_id

    def get_prompts_dataframe(self, prompt_generator: AbstractPromptGenerator = None) -> pd.DataFrame:
        """
        Gets the prompt dataframe containing prompts and completions
        :param prompt_generator: The generator of prompts for the dataset
        :return: The prompt dataframe containing prompts and completions
        """
        if not self.prompt_df:
            assert prompt_generator is not None, "Must provide prompt generator to create prompt dataset for trainer"
            self.prompt_df = self.generate_prompts_dataframe_from_traces(prompt_generator) if self.trace_dataset \
                else self.generate_prompts_dataframe_from_artifacts(prompt_generator)
        return self.prompt_df

    def generate_prompts_dataframe_from_traces(self, prompt_generator: AbstractPromptGenerator) -> pd.DataFrame:
        """
        Converts trace links in to prompt format for generation model.
        :param prompt_generator: The generator of prompts for the dataset
        :return: A prompts based dataset.
        """
        entries = []
        for i, row in self.trace_dataset.trace_df.iterrows():
            source, target = self.trace_dataset.get_link_source_target_artifact(link_id=i)
            entry = prompt_generator.generate(source[ArtifactKeys.CONTENT], target[ArtifactKeys.CONTENT],
                                              label=row[TraceKeys.LABEL.value])
            entries.append(entry)
        return pd.DataFrame(entries)

    def generate_prompts_dataframe_from_artifacts(self, prompt_generator: AbstractPromptGenerator) -> pd.DataFrame:
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
