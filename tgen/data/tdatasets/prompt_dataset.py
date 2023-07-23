import os
import uuid
from typing import Any, Callable, List, Optional, Tuple

import pandas as pd
from tqdm import tqdm

from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.core.trainers.trainer_task import TrainerTask
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.prompt_dataframe import PromptDataFrame
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.prompts.prompt_args import PromptArgs
from tgen.data.prompts.prompt_builder import PromptBuilder
from tgen.data.readers.prompt_project_reader import PromptProjectReader
from tgen.data.summarizer.summarizer import Summarizer
from tgen.data.tdatasets.idataset import iDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.model_manager import ModelManager


class PromptDataset(iDataset):
    """
    Represents a dataset for prompt-based (generative) models such as GPT
    """
    __MAX_SUMMARIZATIONS = 3
    __SAVE_AFTER_N = 100
    __SAVE_FILENAME = "prompt_dataframe_checkpoint.csv"

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
        self.artifact_df = trace_dataset.artifact_df if artifact_df is None and trace_dataset is not None else artifact_df
        self.trace_dataset = trace_dataset
        self.project_file_id = project_file_id
        self.data_export_path = data_export_path
        self.__summarized_artifacts = {}

    def to_hf_dataset(self, model_generator: ModelManager) -> Any:
        """
        Converts data to a Huggingface (HF) Dataset.
        :param model_generator: The model generator determining architecture and feature function for trace links.
        :return: A data in a HF Dataset.
        """
        raise NotImplementedError("A prompt dataset for hugging face is currently not supported")

    def to_trainer_dataset(self, prompt_builder: PromptBuilder) -> pd.DataFrame:
        """
        Converts data to that used by the trainer.
        :param prompt_builder: The prompt generator
        :return: A data used by the trainer.
        """
        return self.get_prompt_dataframe(prompt_builder)

    def to_dataframe(self) -> pd.DataFrame:
        """
        Converts the dataset into a dataframe
        :return: A pandas dataframe of the dataset
        """
        if self.trace_dataset is not None:
            return self.trace_dataset.to_dataframe()
        elif self.artifact_df is not None:
            return self.artifact_df
        elif self.get_prompt_dataframe() is not None:
            return self.get_prompt_dataframe()

    def export_prompt_dataframe(self, prompt_df: pd.DataFrame, export_path: str = None) -> Tuple[str, bool]:
        """
        Exports the prompt dataset
        :param prompt_df: The dataframe containing prompts and completions
        :param export_path: Path to save the prompt dataset to
        :return: The path to the dataset and whether it should be deleted after being used
        """
        export_path = export_path if export_path else self.data_export_path
        should_delete = not export_path
        default_filename = f"prompt_df_{uuid.uuid4()}{PromptProjectReader.FILE_EXT}"
        if export_path:
            if not FileUtil.get_file_ext(export_path):
                export_path = os.path.join(export_path, default_filename)
            FileUtil.create_dir_safely(os.path.dirname(export_path))
        else:
            export_path = os.path.join(os.getcwd(), default_filename)
        prompt_df.to_json(export_path, orient='records', lines=True)
        return export_path, should_delete

    def get_project_file_id(self, llm_manager: AbstractLLMManager, prompt_builder: PromptBuilder = None,
                            summarizer: Summarizer = None) -> str:
        """
        Gets the project file id used by open_ai
        :param llm_manager: The manager of the model that will use the prompts dataset
        :param prompt_builder: The generator of prompts for the dataset
        :param summarizer: If provided, summarizes prompts that exceed the token limit
        :return: The project file id used by open_ai
        """
        if not self.project_file_id:
            prompt_df = self.get_prompt_dataframe(prompt_builder=prompt_builder, prompt_args=llm_manager.prompt_args,
                                                  summarizer=summarizer)
            export_path, should_delete_path = self.export_prompt_dataframe(prompt_df)
            res = llm_manager.upload_file(file=open(export_path), purpose=TrainerTask.TRAIN.value)
            self.project_file_id = res.id
            if should_delete_path:
                os.remove(export_path)
        return self.project_file_id

    def get_prompt_dataframe(self, prompt_builder: PromptBuilder = None, prompt_args: PromptArgs = None,
                             summarizer: Summarizer = None) -> PromptDataFrame:
        """
        Gets the prompt dataframe containing prompts and completions
        :param prompt_args: The arguments for properly formatting the prompt
        :param prompt_builder: The generator of prompts for the dataset
        :param summarizer: If provided, summarizes prompts that exceed the token limit
        :return: The prompt dataframe containing prompts and completions
        """
        if self.prompt_df is None or (prompt_builder and prompt_args):
            generation_method = self._get_generation_method(prompt_args, prompt_builder)
            prompt_entries = generation_method(prompt_builder=prompt_builder, prompt_args=prompt_args, summarizer=summarizer)
            self.prompt_df = PromptDataFrame(prompt_entries)
        return self.prompt_df

    def _get_generation_method(self, prompt_args: PromptArgs, prompt_builder: PromptBuilder) -> Callable:
        """
        Returns the generation method for building prompts.
        :param prompt_args: The prompt configuration for a LLM.
        :param prompt_builder: Contains builders and creates prompts.
        :return: The callable function for creating prompts.
        """
        assert prompt_builder is not None and prompt_args is not None, \
            "Must provide prompt generator to create prompt dataset for trainer"
        if prompt_builder.config.requires_trace_per_prompt:
            assert self.trace_dataset, "Prompt requires traces but no trace dataset was provided"
            return self._generate_prompts_entries_from_traces
        elif prompt_builder.config.requires_artifact_per_prompt:
            assert self._has_trace_data(), "Prompt requires artifacts but no trace dataset or artifact df was provided."
            return self._build_artifact_prompts
        elif prompt_builder.config.requires_all_artifacts:
            assert self._has_trace_data(), "Prompt requires artifacts but no trace dataset or artifact df was provided."
            return self._generate_prompts_entries_from_all_artifacts
        else:
            return self._generate_prompts_dataframe_without_artifacts

    def _generate_prompts_entries_from_traces(self, prompt_builder: PromptBuilder, prompt_args: PromptArgs) -> List:
        """
        Converts trace links in to prompt format for generation model.
        :param prompt_builder: The generator of prompts for the dataset
        :param prompt_args: The arguments for properly formatting the prompt
        :return: A list of prompt entries to use to create dataframe
        """
        entries = []
        traces = self.trace_dataset.trace_df
        save_path = os.path.join(os.getcwd(), self.__SAVE_FILENAME)
        for i, row in tqdm(traces.itertuples(), total=len(traces), desc="Generating prompts dataframe from trace links"):
            if i % self.__SAVE_AFTER_N == 0:
                PromptDataFrame(entries).to_csv(save_path)
            source, target = self.trace_dataset.get_link_source_target_artifact(link_id=i)
            entry = self._create_prompt(prompt_args=prompt_args,
                                        prompt_builder=prompt_builder,
                                        artifacts=[source, target],
                                        label=row[TraceKeys.LABEL])
            entries.append(entry)
        FileUtil.delete_file_safely(save_path)
        return entries

    def _build_artifact_prompts(self, prompt_builder: PromptBuilder, prompt_args: PromptArgs, **kwargs) -> List:
        """
        Creates a prompt for each artifact in project.
        :param prompt_builder: The generator of prompts for the dataset
        :param prompt_args: The arguments for properly formatting the prompt
        :param kwargs: Keyword arguments.
        :return: A list of prompt entries to use to create dataframe
        """
        entries = []
        for id_, artifact in tqdm(self.artifact_df.itertuples(), total=len(self.artifact_df),
                                  desc="Generating prompts dataframe from artifacts"):
            entry = self._create_prompt(prompt_builder=prompt_builder,
                                        prompt_args=prompt_args,
                                        artifact=artifact)
            entries.append(entry)
        return entries

    def _generate_prompts_entries_from_all_artifacts(self, prompt_builder: PromptBuilder, prompt_args: PromptArgs) -> List:
        """
        Converts all artifacts in to prompt format for generation model.
        :param prompt_builder: The generator of prompts for the dataset
        :param prompt_args: The arguments for properly formatting the prompt
        :return: A list of prompt entries to use to create dataframe
        """
        artifacts = [self.artifact_df.get_artifact(art_id) for art_id in self.artifact_df.index]
        prompt_entry = self._create_prompt(prompt_builder=prompt_builder, prompt_args=prompt_args, artifacts=artifacts)
        return [prompt_entry]

    def _generate_prompts_dataframe_without_artifacts(self, prompt_builder: PromptBuilder, prompt_args: PromptArgs,
                                                      summarizer: Summarizer = None) -> List:
        """
        Builds the prompt in the format for generation model without artifacts or traces.
        :param prompt_builder: The generator of prompts for the dataset
        :param prompt_args: The arguments for properly formatting the prompt
        :param summarizer: If provided, summarizes prompts that exceed the token limit
        :return: A list of prompt entries to use to create dataframe
        """
        entry = self._create_prompt(prompt_builder=prompt_builder, prompt_args=prompt_args)
        return [entry]

    @staticmethod
    def _create_prompt(prompt_builder: PromptBuilder, prompt_args: PromptArgs, **prompt_kwargs) -> Optional[EnumDict]:
        """
        Creates a prompt entry using the given builder.
        :param prompt_builder: Builds the prompt.
        :param prompt_args: Configures the prompt for some LLM.
        :param prompt_kwargs: Keyword arguments passed to `build` method.
        :return: The prompt entry
        """
        entry = prompt_builder.build(model_format_args=prompt_args, **prompt_kwargs)

        # TODO: in the future may need to shorten if entry exceeds token limit but generally doesn't exceed limit for current models
        return entry

    def _get_artifact_summarization(self, artifact: EnumDict, summarizer: Summarizer, force_create_new: bool = False) -> str:
        """
        Gets a summarization of the artifact from cache if it exists, otherwise creates a summarization
        :param artifact: The artifact to summarize
        :param summarizer: The summarizer to use
        :return: The summarized content
        """
        artifact_id = artifact[ArtifactKeys.ID]
        if artifact_id not in self.__summarized_artifacts:
            summary = summarizer.summarize_single(content=artifact[ArtifactKeys.CONTENT], id_=artifact_id)
            self.__summarized_artifacts[artifact_id] = summary
            return summary
        if force_create_new:
            summary = summarizer.summarize_single(content=self.__summarized_artifacts[artifact_id], id_=artifact_id)
            return summary
        return self.__summarized_artifacts[artifact_id]

    def _has_trace_data(self) -> bool:
        """
        Returns True when project data in the form of an artifacts_df or trace_dataset has been provided, else False
        :return: True when project data in the form of an artifacts_df or trace_dataset has been provided, else False
        """
        return not (self.artifact_df is None and self.trace_dataset is None)

    def __getattr__(self, item: str) -> Any:
        """
        Overriding to allow direct access to trace dataset elements
        :param item: The attribute name to get
        :return: The attribute from trace dataset if it exists else attribute error is raised
        """
        if hasattr(self.trace_dataset, item):
            return getattr(self.trace_dataset, item)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")
