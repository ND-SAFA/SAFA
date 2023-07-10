import os
import re
import uuid
from datetime import datetime
from typing import Any, Dict, List, Set, Type, Union

import pandas as pd

from tgen.constants.deliminator_constants import EMPTY_STRING, NEW_LINE
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.exporters.abstract_dataset_exporter import AbstractDatasetExporter
from tgen.data.exporters.csv_exporter import CSVExporter
from tgen.data.exporters.dataframe_exporter import DataFrameExporter
from tgen.data.keys.csv_keys import CSVKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.prompts.artifact_prompt import ArtifactPrompt
from tgen.data.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_builder import PromptBuilder
from tgen.data.prompts.prompt_response_manager import PromptResponseManager, REQUIRE_ALL_TAGS
from tgen.data.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.data.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.train.trainers.llm_trainer import LLMTrainer
from tgen.util.dict_util import DictUtil
from tgen.util.file_util import FileUtil
from tgen.util.logging.logger_manager import logger
from tgen.train.trainers.llm_trainer_state import LLMTrainerState


def save_dataset_checkpoint(dataset: Any, export_path: str = None,
                            filename: str = None, exporter_class: Type[AbstractDatasetExporter] = None) -> str:
    """
    Exports the dataset to csv
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
    if not isinstance(dataset, TraceDataset) and not isinstance(dataset, pd.DataFrame):
        FileUtil.write_yaml(dataset, full_export_path)
    else:
        if isinstance(dataset, PromptDataset) and dataset.trace_dataset is not None:
            dataset = dataset.trace_dataset
        if exporter_class is None:
            exporter_class = DataFrameExporter if isinstance(dataset, TraceDataset) else CSVExporter
        if issubclass(exporter_class, CSVExporter):
            full_export_path += CSVKeys.EXT
        exporter = exporter_class(export_path=full_export_path, dataset=dataset)
        exporter.export()
    logger.info(f"Dataset checkpoint saved to {full_export_path} ")
    return full_export_path


def get_predictions(prompt_builder: PromptBuilder,
                    dataset: PromptDataset,
                    llm_manager: AbstractLLMManager,
                    max_tokens: int,
                    response_prompt_ids: Union[Set, str] = None, tags_for_response: Union[Set, str] = None,
                    return_first: bool = False, export_path: str = None) -> Dict[str, str]:
    """
    Gets the predictions for the given prompts on the given dataset
    :param prompt_builder: Builds the prompts for the model
    :param dataset: The dataset to use with the prompts
    :param llm_manager: The LLM manager to use for predictions
    :param max_tokens: The max tokens for the model
    :param response_prompt_ids: The prompt id to extract from predictions
    :param tags_for_response: The tag to extract from predictions
    :param return_first: If True, returns the first item from each list of parsed tags (often there is only one per tag)
    :param export_path: The path to export predictions to
    :return: The model predictions
    """
    load = True
    llm_manager.llm_args.set_max_tokens(max_tokens)
    dataset_manager = TrainerDatasetManager.create_from_datasets({DatasetRole.EVAL: dataset})
    trainer = LLMTrainer(LLMTrainerState(llm_manager=llm_manager,
                                         trainer_dataset_manager=dataset_manager,
                                         prompt_builder=prompt_builder,
                                         completion_type=LLMCompletionType.GENERATION))
    if export_path and "artifact_gen_response" in export_path and load:
        predictions = FileUtil.read_yaml("/home/kat/git-repos/safa/tgen/output/hgen/bend/c6c75924-5e05-45dc-aa0e-df449842bd54/"
                                         "artifact_gen_response.yaml")
        response_prompt_ids = {"0667b783-7fbc-47b0-90eb-1252f9fa0f85", "e0c0bd4e-0169-426a-bce7-a19b144b82fe"}
    elif export_path and "gen_refinement_response" in export_path and load:
        predictions = FileUtil.read_yaml("/home/kat/git-repos/safa/tgen/output/hgen/bend/c6c75924-5e05-45dc-aa0e-df449842bd54/"
                                         "gen_refinement_response1.yaml")
        response_prompt_ids = {"b3832f3e-4b8e-43d4-971a-78f23d9d3402"}
    else:
        predictions = trainer.perform_prediction().predictions

    if export_path:
        base_name, file_name = os.path.split(export_path)
        save_dataset_checkpoint(predictions, export_path=base_name, filename=file_name)

    response_prompt_ids = {response_prompt_ids} if isinstance(response_prompt_ids, str) else response_prompt_ids
    if response_prompt_ids:
        predictions = [DictUtil.combine_child_dicts(p, response_prompt_ids) for p in predictions]
        if tags_for_response:
            predictions = [DictUtil.filter_dict_keys(p, keys2keep=tags_for_response) if isinstance(tags_for_response, set)
                           else p[tags_for_response] for p in predictions]
            if return_first:
                if isinstance(predictions[0], dict):
                    predictions = [{key: value[0] if isinstance(value, list) else value for key, value in p.items()}
                                   for p in predictions]
                else:
                    predictions = [p[0] for p in predictions]
    return predictions


def create_artifact_df_from_generated_artifacts(hgen_args: HGenArgs, artifact_generations: List[str], target_layer_id: str,
                                                generate_names: bool = True) -> ArtifactDataFrame:
    """
    Creates a dataframe with new artifacts generated to fill in an upper level of the hierarchy
    :param hgen_args: The arguments for the hierarchy generation
    :param artifact_generations: A list of generated artifact content
    :param target_layer_id: The id for the layer with the new generated artifacts
    :param generate_names: If True, generates names for the new artifacts
    :return: The dataframe of generated artifacts
    """
    new_artifact_df = ArtifactDataFrame({ArtifactKeys.ID: [str(uuid.uuid4()) for _ in artifact_generations],
                                         ArtifactKeys.CONTENT: artifact_generations,
                                         ArtifactKeys.LAYER_ID: [target_layer_id for _ in artifact_generations]})
    if generate_names:
        try:
            logger.info(f"Creating names for {len(new_artifact_df)} {hgen_args.target_type}\n")
            name_prompt = Prompt(f"Create a name for this {hgen_args.target_type}.",
                                 PromptResponseManager(response_tag="name", required_tag_ids=REQUIRE_ALL_TAGS))
            artifact_prompt = ArtifactPrompt(include_id=False)
            prompt_builder = PromptBuilder(prompts=[name_prompt, artifact_prompt])
            dataset = PromptDataset(artifact_df=new_artifact_df)
            names = get_predictions(prompt_builder,
                                    dataset,
                                    hgen_args.hgen_llm_manager,
                                    hgen_args.artifact_name_tokens,
                                    response_prompt_ids=name_prompt.id,
                                    tags_for_response=name_prompt.response_manager.response_tag,
                                    return_first=True)
            names = [name.replace(NEW_LINE, EMPTY_STRING).strip() for name in names]
            assert len(set(names)) == len(names), f"Found duplicates names: {names}"
            assert len(names) == len(new_artifact_df.index), "Number of predicted names does not match number of artifacts"
            new_artifact_df.index = names
        except Exception:
            logger.exception("Unable to generate names for the artifacts")
    return new_artifact_df


def _get_prompt_builder_for_generation(hgen_args: HGenArgs,
                                       task_prompt: Union[QuestionnairePrompt, Prompt],
                                       base_prompt: SupportedPrompts = SupportedPrompts.HGEN_GENERATION,
                                       summary_prompt: Prompt = None, artifact_type: str = None) -> PromptBuilder:
    """
    Gets the prompt builder used for the generations
    :param task_prompt: The questionnaire prompt given to the model to produce the generations
    :param base_prompt: The main prompt that starts the prompt
    :param summary_prompt: Instructions for the model to create a summary of the system first
    :return: The prompt builder used for the generations
    """
    generation_step_response_manager = task_prompt.question_prompts[-1].response_manager if isinstance(task_prompt,
                                                                                                       QuestionnairePrompt) \
        else task_prompt.response_manager
    generation_step_response_manager.formatter = lambda tag, val: parse_generated_artifacts(val)

    artifact_prompt = MultiArtifactPrompt(prompt_start=format_as_markdown("{artifact_type}S:"),
                                          build_method=MultiArtifactPrompt.BuildMethod.NUMBERED,
                                          include_ids=False, data_type=MultiArtifactPrompt.DataType.ARTIFACT)
    artifact_type = hgen_args.source_type if not artifact_type else artifact_type
    artifact_prompt.format_value(artifact_type=artifact_type.upper())
    prompts = [base_prompt.value, artifact_prompt]

    task_preface = f"{NEW_LINE}{format_as_markdown('TASKS:')}{NEW_LINE}"
    if summary_prompt:
        summary_prompt.value = task_preface + summary_prompt.value
        prompts.append(summary_prompt)
    else:
        task_prompt.value = task_preface + task_prompt.value

    prompts.append(task_prompt)
    prompt_builder = PromptBuilder(prompts)
    prompt_builder.format_prompts_with_var(source_type=hgen_args.source_type, target_type=hgen_args.target_type)
    return prompt_builder


def parse_generated_artifacts(res: str) -> List[str]:
    """
    Parses the model response into a list of the artifact content.
    :param res: The response from the model containing the generated artifact content
    :return: The list of the generated artifact content
    """
    return [re.sub(r'^\d+\.\s', '', content).strip() for content in res.split(NEW_LINE) if len(content) > 1]


def format_as_markdown(string: str, level: int = 1) -> str:
    """
    Formats the string as markdown header
    :param string: The string to format
    :param level: The level of the header
    :return: The string formatted as markdown
    """
    return f"{'#' * level} {string}"


def _convert_spaces_to_dashes(str2convert) -> str:
    """
    Converts the str to use dashes instead of spaces
    :return: The str with dashes instead of spaces
    """
    return "-".join(str2convert.split()).lower()
