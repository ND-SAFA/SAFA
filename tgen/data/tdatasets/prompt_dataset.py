import os
import uuid
from typing import Any, Callable, List, Optional, Tuple, Union

import pandas as pd
from tqdm import tqdm

from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.core.trainers.trainer_task import TrainerTask
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.prompt_dataframe import PromptDataFrame
from tgen.data.exporters.safa_exporter import SafaExporter
from tgen.data.keys.structure_keys import TraceKeys
from tgen.data.readers.prompt_project_reader import PromptProjectReader
from tgen.data.readers.structured_project_reader import StructuredProjectReader
from tgen.data.tdatasets.idataset import iDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.model_manager import ModelManager
from tgen.prompts.llm_prompt_build_args import LLMPromptBuildArgs
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.summarizer.summary import Summary


class PromptDataset(iDataset):
    """
    Represents a dataset for prompt-based (generative) models such as GPT
    """
    __MAX_SUMMARIZATIONS = 3
    __SAVE_AFTER_N = 100
    __SAVE_FILENAME = "prompt_dataframe_checkpoint.csv"

    def __init__(self, prompt_df: PromptDataFrame = None, artifact_df: ArtifactDataFrame = None,
                 trace_dataset: TraceDataset = None, project_file_id: str = None, data_export_path: str = None,
                 project_summary: Summary = None):
        """
        Initializes the dataset with necessary artifact/trace information and generator for the prompts
        :param prompt_df: The prompt dataframe
        :param artifact_df: The dataframe containing project artifacts
        :param trace_dataset: The dataset containing trace links and artifacts
        :param project_file_id: The file id used by open AI
        :param data_export_path: The path to where data files will be saved if specified. May be to a directory or specific file
        :param project_summary: Default project summary to use.
        """
        self.prompt_df = prompt_df
        self.artifact_df = trace_dataset.artifact_df if artifact_df is None and trace_dataset is not None else artifact_df
        self.trace_dataset = trace_dataset
        self.project_file_id = project_file_id
        self.data_export_path = data_export_path
        self.project_summary = project_summary
        self.__state_has_changed = True

    def to_hf_dataset(self, model_generator: ModelManager) -> Any:
        """
        Converts data to a Huggingface (HF) Dataset.
        :param model_generator: The model generator determining architecture and feature function for trace links.
        :return: A data in a HF Dataset.
        """
        raise NotImplementedError("A prompt dataset for hugging face is currently not supported")

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
        else:
            raise NotImplementedError("Cannot convert to dataframe without trace data or prompt dataframe")

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

    def get_project_file_id(self, llm_manager: AbstractLLMManager, prompt_builder: PromptBuilder = None) -> str:
        """
        Gets the project file id used by open_ai
        :param llm_manager: The manager of the model that will use the prompts dataset
        :param prompt_builder: The generator of prompts for the dataset
        :return: The project file id used by open_ai
        """
        if not self.project_file_id:
            prompt_df = self.get_prompt_dataframe(prompt_builders=prompt_builder, prompt_args=llm_manager.prompt_args)
            export_path, should_delete_path = self.export_prompt_dataframe(prompt_df)
            res = llm_manager.upload_file(file=open(export_path), purpose=TrainerTask.TRAIN.value)
            self.project_file_id = res.concept_id
            if should_delete_path:
                os.remove(export_path)
        return self.project_file_id

    def get_prompt_dataframe(self, prompt_builders: Union[List[PromptBuilder], PromptBuilder] = None,
                             prompt_args: LLMPromptBuildArgs = None) -> PromptDataFrame:
        """
        Gets the prompt dataframe containing prompts and completions
        :param prompt_args: The arguments for properly formatting the prompt
        :param prompt_builders: The generator of prompts for the dataset
        :return: The prompt dataframe containing prompts and completions
        """
        if self.prompt_df is None or (prompt_builders and prompt_args):
            if not isinstance(prompt_builders, list):
                prompt_builders = [prompt_builders]
            prompt_entries = []
            for prompt_builder in prompt_builders:
                generation_method = self._get_generation_method(prompt_args, prompt_builder)
                prompt_entries.extend(generation_method(prompt_builder=prompt_builder, prompt_args=prompt_args))
            self.prompt_df = PromptDataFrame(prompt_entries)
        return self.prompt_df

    def as_creator(self, project_path: str):
        """
        Converts the dataset into a creator that can remake it
        :param project_path: The path to save the dataset at for reloading
        :param dataset_dirname: The directory that the dataset will be saved to
        :return: The dataset creator
        """
        from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
        from tgen.data.exporters.prompt_dataset_exporter import PromptDatasetExporter
        if not os.path.exists(project_path) or self.__state_has_changed:
            PromptDatasetExporter(export_path=project_path, trace_dataset_exporter_type=SafaExporter, dataset=self).export()
        collapsed_path = FileUtil.collapse_paths(project_path)
        if self.trace_dataset is not None:
            prompt_creator = PromptDatasetCreator(trace_dataset_creator=TraceDatasetCreator(StructuredProjectReader(collapsed_path)))
        elif self.artifact_df is not None:
            from tgen.data.readers.artifact_project_reader import ArtifactProjectReader
            prompt_creator = PromptDatasetCreator(project_reader=ArtifactProjectReader(project_path=collapsed_path))
        else:
            raise NotImplementedError("Cannot get creator for prompt dataset without an artifact df or trace dataset")
        self.__state_has_changed = False
        return prompt_creator

    def update_artifact_df(self, artifact_df: ArtifactDataFrame) -> None:
        """
        Updates the artifact dataframe of the prompt dataset as well as the trace dataset if it exists
        :param artifact_df: The artifact df to replace the existing one with
        :return: None
        """
        self.artifact_df = artifact_df
        if self.trace_dataset is not None:
            self.trace_dataset.artifact_df = artifact_df
        self.__state_has_changed = True

    def _get_generation_method(self, prompt_args: LLMPromptBuildArgs, prompt_builder: PromptBuilder) -> Callable:
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

    def _generate_prompts_entries_from_traces(self, prompt_builder: PromptBuilder, prompt_args: LLMPromptBuildArgs) -> List:
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
            source[TraceKeys.SOURCE] = True
            target[TraceKeys.TARGET] = True
            entry = self._create_prompt(prompt_args=prompt_args,
                                        prompt_builder=prompt_builder,
                                        artifacts=[source, target],
                                        label=row[TraceKeys.LABEL])
            entries.append(entry)
        FileUtil.delete_file_safely(save_path)
        return entries

    def _build_artifact_prompts(self, prompt_builder: PromptBuilder, prompt_args: LLMPromptBuildArgs, **kwargs) -> List:
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

    def _generate_prompts_entries_from_all_artifacts(self, prompt_builder: PromptBuilder, prompt_args: LLMPromptBuildArgs) -> List:
        """
        Converts all artifacts in to prompt format for generation model.
        :param prompt_builder: The generator of prompts for the dataset
        :param prompt_args: The arguments for properly formatting the prompt
        :return: A list of prompt entries to use to create dataframe
        """
        artifacts = [self.artifact_df.get_artifact(art_id) for art_id in self.artifact_df.index]
        prompt_entry = self._create_prompt(prompt_builder=prompt_builder, prompt_args=prompt_args, artifacts=artifacts)
        return [prompt_entry]

    def _generate_prompts_dataframe_without_artifacts(self, prompt_builder: PromptBuilder, prompt_args: LLMPromptBuildArgs) -> List:
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
    def _create_prompt(prompt_builder: PromptBuilder, prompt_args: LLMPromptBuildArgs, **prompt_kwargs) -> Optional[EnumDict]:
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

    def _has_trace_data(self) -> bool:
        """
        Returns True when project data in the form of an artifact_df or trace_dataset has been provided, else False
        :return: True when project data in the form of an artifact_df or trace_dataset has been provided, else False
        """
        return not (self.artifact_df is None and self.trace_dataset is None)

    def __getattr__(self, item: str) -> Any:
        """
        Overriding to allow direct access to trace dataset elements
        :param item: The attribute name to get
        :return: The attribute from trace dataset if it exists else attribute error is raised
        """
        if not item.startswith("__"):
            try:
                return getattr(self.trace_dataset, item)
            except Exception as e:
                pass
        raise AttributeError(f"{self.__class__.__name__} object has no attribute {item}")
