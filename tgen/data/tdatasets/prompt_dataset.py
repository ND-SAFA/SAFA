import os
import uuid
from typing import Any, Optional, Tuple

import pandas as pd
from tqdm import tqdm

from tgen.constants.deliminator_constants import EMPTY_STRING
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.prompt_dataframe import PromptDataFrame
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.abstract_prompt_creator import AbstractPromptCreator
from tgen.data.prompts.classification_prompt_creator import ClassificationPromptCreator
from tgen.data.readers.prompt_project_reader import PromptProjectReader
from tgen.data.chunkers.natural_language_chunker import NaturalLanguageChunker
from tgen.data.summarizer.summarizer import Summarizer
from tgen.data.tdatasets.idataset import iDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.models.model_manager import ModelManager
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.ai.open_ai_util import OpenAIUtil
from tgen.util.enum_util import EnumDict
from tgen.util.file_util import FileUtil


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
        if not self.project_file_id and prompt_df is None:
            assert self._has_trace_data(), "Either artifacts dataframe or trace dataframe must be provided to generate dataset."
        self.__summarized_artifacts = {}

    def to_hf_dataset(self, model_generator: ModelManager) -> Any:
        """
        Converts data to a Huggingface (HF) Dataset.
        :param model_generator: The model generator determining architecture and feature function for trace links.
        :return: A data in a HF Dataset.
        """
        raise NotImplementedError("A prompt dataset for hugging face is currently not supported")

    def to_trainer_dataset(self, prompts_generator: AbstractPromptCreator) -> pd.DataFrame:
        """
        Converts data to that used by Huggingface (HF) trainer.
        :param prompts_generator: The model generator determining architecture and feature function for trace links.
        :return: A data used by the HF trainer.
        """
        return self.get_prompts_dataframe(prompts_generator)

    def to_dataframe(self) -> pd.DataFrame:
        """
        Converts the dataset into a dataframe
        :return: A pandas dataframe of the dataset
        """
        if self.trace_dataset is not None:
            return self.trace_dataset.to_dataframe()
        elif self.artifact_df is not None:
            return self.artifact_df
        elif self.get_prompts_dataframe() is not None:
            return self.get_prompts_dataframe()

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

    def get_project_file_id(self, prompt_creator: AbstractPromptCreator = None, summarizer: Summarizer = None) -> str:
        """
        Gets the project file id used by open_ai
        :param prompt_creator: The generator of prompts for the dataset
        :param summarizer: If provided, summarizes prompts that exceed the token limit
        :return: The project file id used by open_ai
        """
        if not self.project_file_id:
            prompt_df = self.get_prompts_dataframe(prompt_creator, summarizer)
            export_path, should_delete_path = self.export_prompt_dataframe(prompt_df)
            res = OpenAIUtil.upload_file(file=open(export_path), purpose=TrainerTask.TRAIN.value)
            self.project_file_id = res.id
            if should_delete_path:
                os.remove(export_path)
        return self.project_file_id

    def get_prompts_dataframe(self, prompt_creator: AbstractPromptCreator = None, summarizer: Summarizer = None) -> pd.DataFrame:
        """
        Gets the prompt dataframe containing prompts and completions
        :param prompt_creator: The generator of prompts for the dataset
        :param summarizer: If provided, summarizes prompts that exceed the token limit
        :return: The prompt dataframe containing prompts and completions
        """
        if self.prompt_df is None:
            assert prompt_creator is not None, "Must provide prompt generator to create prompt dataset for trainer"
            assert self._has_trace_data(), "Either artifacts dataframe or trace dataset" \
                                           " to generate dataframe."
            self.prompt_df = self._generate_prompts_dataframe_from_traces(prompt_creator, summarizer) \
                if self.trace_dataset and isinstance(prompt_creator, ClassificationPromptCreator) else \
                self._generate_prompts_dataframe_from_artifacts(prompt_creator, summarizer)
        return self.prompt_df

    def _generate_prompts_dataframe_from_traces(self, prompt_creator: AbstractPromptCreator,
                                                summarizer: Summarizer = None) -> pd.DataFrame:
        """
        Converts trace links in to prompt format for generation model.
        :param prompt_creator: The generator of prompts for the dataset
        :param summarizer: If provided, summarizes prompts that exceed the token limit
        :return: A prompts based dataset.
        """
        entries = []
        traces = self.trace_dataset.trace_df
        save_path = os.path.join(os.getcwd(), self.__SAVE_FILENAME)
        for i, row in tqdm(traces.itertuples(), total=len(traces), desc="Generating prompts dataframe from trace links"):
            if i % self.__SAVE_AFTER_N == 0:
                PromptDataFrame(entries).to_csv(save_path)
            source, target = self.trace_dataset.get_link_source_target_artifact(link_id=i)
            entry = self._get_prompt_entry(source_artifact=source, target_artifact=target,
                                           label=row[TraceKeys.LABEL], prompt_creator=prompt_creator, summarizer=summarizer)
            entries.append(entry)
        FileUtil.delete_file_safely(save_path)
        return PromptDataFrame(entries)

    def _generate_prompts_dataframe_from_artifacts(self, prompt_creator: AbstractPromptCreator,
                                                   summarizer: Summarizer = None) -> pd.DataFrame:
        """
        Converts artifacts in to prompt format for generation model.
        :param prompt_creator: The generator of prompts for the dataset
        :param summarizer: If provided, summarizes prompts that exceed the token limit
        :return: A prompts based dataset.
        """
        entries = []
        for i, artifact in tqdm(self.artifact_df.itertuples(), total=len(self.artifact_df),
                                desc="Generating prompts dataframe from artifacts"):
            entry = self._get_prompt_entry(target_artifact=artifact, source_artifact=None, prompt_creator=prompt_creator,
                                           summarizer=summarizer)
            entries.append(entry)
        return PromptDataFrame(entries)

    def _get_prompt_entry(self, target_artifact: EnumDict, prompt_creator: AbstractPromptCreator, source_artifact: EnumDict = None,
                          summarizer: Summarizer = None, **prompt_creator_params) -> Optional[EnumDict]:
        """
        Creates a prompt entry using the given creator and summarizing if the prompt exceeds the token limit and a summarizer is given
        :param source_content: The content of the source artifact
        :param target_content: The content of the target artifact
        :param prompt_creator: The creator used to generate the prompt
        :param summarizer: The summarizer responsible for shortening prompts if they exceed the token limit
        :param prompt_creator_params: Additional params to give the prompt creator
        :return: The prompt entry
        """
        source_content = source_artifact[ArtifactKeys.CONTENT] if source_artifact else EMPTY_STRING
        entry = prompt_creator.create(source_content=source_content,
                                      target_content=target_artifact[ArtifactKeys.CONTENT], **prompt_creator_params)
        if not summarizer:
            return entry

        # Ensure prompt fits in token limit
        for i in range(self.__MAX_SUMMARIZATIONS):
            if not summarizer.exceeds_token_limit(entry[PromptKeys.PROMPT] + entry[PromptKeys.COMPLETION]):
                break
            force_create_new_summarization = i > 0
            if source_artifact:
                source_content = self._get_artifact_summarization(source_artifact, summarizer, force_create_new_summarization)
            target_content = self._get_artifact_summarization(target_artifact, summarizer, force_create_new_summarization)
            entry = prompt_creator.create(source_content, target_content, **prompt_creator_params)
        if summarizer.exceeds_token_limit(entry[PromptKeys.PROMPT] + entry[PromptKeys.COMPLETION]):
            # Since summarization failed, just cut off anything that exceeds the limit
            chunker = NaturalLanguageChunker(model_name=summarizer.model_for_token_limit)
            entry[PromptKeys.PROMPT] = chunker.chunk(entry[PromptKeys.PROMPT])[0]
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
            summary = summarizer.summarize(content=artifact[ArtifactKeys.CONTENT], id_=artifact_id)
            self.__summarized_artifacts[artifact_id] = summary
            return summary
        if force_create_new:
            summary = summarizer.summarize(content=self.__summarized_artifacts[artifact_id], id_=artifact_id)
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
