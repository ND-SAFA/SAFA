import os
import re
from typing import Dict, List, Set, Tuple, Union

import pandas as pd
from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.keys.structure_keys import ArtifactKeys
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.llm.llm_task import LLMCompletionType
from common_resources.tools.constants.symbol_constants import DASH, EMPTY_STRING, NEW_LINE

from common_resources.tools.t_logging.logger_manager import logger
from common_resources.tools.util.file_util import FileUtil
from common_resources.tools.util.llm_response_util import LLMResponseUtil
from common_resources.tools.util.prompt_util import PromptUtil
from common_resources.tools.util.str_util import StrUtil
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.hgen.hgen_args import HGenArgs, PredictionStep
from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts

TASK_PREFACE = f"{NEW_LINE} # TASKS:{NEW_LINE}"
SAVE_DATASET_DIRNAME = "final_generated_dataset"


class HGenUtil:

    @staticmethod
    def get_predictions(prompt_builder: PromptBuilder, hgen_args: HGenArgs,
                        prediction_step: PredictionStep, dataset: PromptDataset = None,
                        response_prompt_ids: Union[Set, str] = None, tags_for_response: Union[Set, str] = None,
                        return_first: bool = False, export_path: str = None) -> Union[List[Dict], Dict[str, str]]:
        """
        Gets the predictions for the given prompts on the given dataset
        :param prompt_builder: Builds the prompts for the model
        :param dataset: The dataset to use with the prompts
        :param prediction_step: The prediction step currently being run
        :param hgen_args: The args for the hierarchy generation
        :param response_prompt_ids: The prompt id to extract from predictions
        :param tags_for_response: The tag to extract from predictions
        :param return_first: If True, returns the first item from each list of parsed tags (often there is only one per tag)
        :param export_path: The path to export predictions to
        :return: The model predictions
        """
        max_tokens = hgen_args.max_tokens[prediction_step.value]
        llm_manager = hgen_args.llm_managers[prediction_step.value]
        llm_manager.llm_args.set_max_tokens(max_tokens)

        tags_for_response = tags_for_response.pop() \
            if isinstance(tags_for_response, set) and len(tags_for_response) == 1 else tags_for_response
        base_name, file_name = os.path.split(export_path) if export_path else (EMPTY_STRING, EMPTY_STRING)

        load_path = FileUtil.safely_join_paths(hgen_args.load_dir, file_name)
        load_path = FileUtil.add_ext(load_path, FileUtil.YAML_EXT) if load_path else load_path
        if dataset is None:
            predictions = LLMTrainer.predict_from_prompts(llm_manager=llm_manager, prompt_builders=prompt_builder,
                                                          save_and_load_path=load_path).predictions
        else:
            dataset_manager = TrainerDatasetManager.create_from_datasets(eval=dataset)
            trainer = LLMTrainer(LLMTrainerState(llm_manager=llm_manager,
                                                 trainer_dataset_manager=dataset_manager,
                                                 prompt_builders=prompt_builder,
                                                 completion_type=LLMCompletionType.GENERATION))
            predictions = trainer.perform_prediction(save_and_load_path=load_path).predictions

        predictions = LLMResponseUtil.extract_predictions_from_response(predictions=predictions,
                                                                        response_prompt_ids=response_prompt_ids,
                                                                        return_first=return_first,
                                                                        tags_for_response=tags_for_response)
        return predictions

    @staticmethod
    def create_artifact_df_from_generated_artifacts(hgen_args: HGenArgs,
                                                    generations2sources: Dict[str, Set],
                                                    target_layer_id: str,
                                                    generate_names: bool = True,
                                                    generation_id: Union[int, str] = 0) -> Tuple[ArtifactDataFrame, Dict[str, Set]]:
        """
        Creates a dataframe with new artifacts generated to fill in an upper level of the hierarchy
        :param hgen_args: The arguments for the hierarchy generation
        :param generations2sources: A dictionary mapping generated artifact content to the predicted links
        :param target_layer_id: The id for the layer with the new generated artifacts
        :param generate_names: If True, generates names for the new artifacts
        :param generation_id: How many times has the name generation currently run.
        :return: The dataframe of generated artifacts and a dictionary mapping the new name to the list of predicted related artifacts
        """
        filename = f"artifact_names_{generation_id}.yaml"
        new_artifact_df = ArtifactDataFrame({ArtifactKeys.ID: [f"{StrUtil.get_letter_from_number(i)}{i}"
                                                               for i in range(len(generations2sources))],
                                             ArtifactKeys.CONTENT: list(generations2sources.keys()),
                                             ArtifactKeys.LAYER_ID: [target_layer_id for _ in generations2sources]})
        if generate_names:
            try:
                use_content_as_names = {i: content
                                        for i, content in enumerate(new_artifact_df[ArtifactKeys.CONTENT])
                                        if len(content.split()) <= 5}

                if len(use_content_as_names) == len(new_artifact_df):
                    names = list(use_content_as_names.values())
                else:
                    logger.info(f"Creating names for {len(new_artifact_df)} {hgen_args.target_type}\n")
                    name_prompt: Prompt = SupportedPrompts.HGEN_TITLE_PROMPT.value
                    name_prompt.format_value(target_type=hgen_args.target_type)
                    artifact_prompt = ArtifactPrompt(include_id=False, build_method=ArtifactPrompt.BuildMethod.XML)
                    prompt_builder = PromptBuilder(prompts=[name_prompt, artifact_prompt])
                    dataset = PromptDataset(artifact_df=new_artifact_df)
                    predictions_path = FileUtil.safely_join_paths(hgen_args.export_dir, filename)
                    names = HGenUtil.get_predictions(prompt_builder, hgen_args=hgen_args,
                                                     prediction_step=PredictionStep.NAME,
                                                     dataset=dataset, response_prompt_ids=name_prompt.args.prompt_id,
                                                     tags_for_response=name_prompt.response_manager.response_tag,
                                                     return_first=True,
                                                     export_path=predictions_path)
                    assert len(names) == len(new_artifact_df.index), "Number of predicted names does not match number of artifacts"
                    names = [name if i not in use_content_as_names else use_content_as_names[i] for i, name in enumerate(names)]
                names = [HGenUtil.format_names(n, index=i, target_type=target_layer_id) for i, n in enumerate(names)]
                new_artifact_df.index = pd.Index(names, name=new_artifact_df.index_name())
            except Exception:
                logger.exception("Unable to generate names for the artifacts")
        name_2_related_children = {name: links for name, links in
                                   zip(new_artifact_df.index, list(generations2sources.values()))}
        return new_artifact_df, name_2_related_children

    @staticmethod
    def format_names(name: str, target_type: str, index: int) -> str:
        """
        Formats the names with the initials of the target type
        :param name: The name of the artifact
        :param target_type: The type of artifact
        :param index: The index of the artifact with the corresponding name
        :return: The formatted name with the initials of the target type
        """
        initials = HGenUtil.get_initials(target_type)
        id_format = f"[{initials}{index + 1}]"
        return f"{id_format} {PromptUtil.strip_new_lines_and_extra_space(name)}"

    @staticmethod
    def parse_generated_artifacts(res: str) -> List[str]:
        """
        Parses the model response into a list of the artifact content.
        :param res: The response from the model containing the generated artifact content
        :return: The list of the generated artifact content
        """
        return [re.sub(r'^\d+\.\s', '', content).strip(DASH).strip() for content in res.split(NEW_LINE) if
                len(content) > 1]

    @staticmethod
    def convert_spaces_to_dashes(str2convert: str) -> str:
        """
        Converts the str to use dashes instead of spaces
        :param str2convert: The string to process.
        :return: The str with dashes instead of spaces
        """
        return DASH.join(str2convert.split()).lower()

    @staticmethod
    def get_initials(input_string: str) -> str:
        """
        Creates a string with the first letter of each word
        :param input_string: The input string
        :return: The first letter of each word
        """
        words = input_string.split()
        if len(words) <= 1:
            return input_string
        first_letters = [word[0] for word in words]
        return EMPTY_STRING.join(first_letters).upper()

    @staticmethod
    def get_ranking_dir(directory: str) -> str:
        """
        Get the directory for ranking job
        :param directory: The main directory used by hgen
        :return: The full path
        """
        return FileUtil.safely_join_paths(directory, "ranking")
