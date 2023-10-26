import os
import re
from typing import Dict, List, Set, Tuple, Union

from tgen.common.constants.deliminator_constants import DASH, EMPTY_STRING, NEW_LINE
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.common.util.llm_response_util import LLMResponseUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.prompt_util import PromptUtil
from tgen.core.trainers.llm_trainer import LLMTrainer
from tgen.core.trainers.llm_trainer_state import LLMTrainerState
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.hgen_args import HGenArgs, PredictionStep
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.context_prompt import ContextPrompt
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.prompt_response_manager import PromptResponseManager, REQUIRE_ALL_TAGS
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
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

        load_path = FileUtil.add_ext(os.path.join(hgen_args.load_dir, file_name), FileUtil.YAML_EXT) \
            if file_name and hgen_args.load_dir else EMPTY_STRING
        if dataset is None:
            predictions = LLMTrainer.predict_from_prompts(llm_manager=llm_manager, prompt_builder=prompt_builder,
                                                          save_and_load_path=load_path).predictions
        else:
            dataset_manager = TrainerDatasetManager.create_from_datasets({DatasetRole.EVAL: dataset})
            trainer = LLMTrainer(LLMTrainerState(llm_manager=llm_manager,
                                                 trainer_dataset_manager=dataset_manager,
                                                 prompt_builder=prompt_builder,
                                                 completion_type=LLMCompletionType.GENERATION))
            predictions = trainer.perform_prediction(save_and_load_path=load_path).predictions

        predictions = LLMResponseUtil.extract_predictions_from_response(predictions=predictions,
                                                                        response_prompt_ids=response_prompt_ids,
                                                                        return_first=return_first,
                                                                        tags_for_response=tags_for_response)
        return predictions

    @staticmethod
    def get_prompt_builder_for_generation(hgen_args: HGenArgs,
                                          task_prompt: Union[QuestionnairePrompt, Prompt],
                                          base_prompt: Union[SupportedPrompts, str] = SupportedPrompts.HGEN_GENERATION,
                                          summary_prompt: Prompt = None, artifact_type: str = None,
                                          combine_summary_and_task_prompts: bool = False,
                                          build_method: MultiArtifactPrompt.BuildMethod = MultiArtifactPrompt.BuildMethod.XML,
                                          id_to_context_artifacts: Dict[str, List[EnumDict]] = None
                                          ) -> PromptBuilder:
        """
        Gets the prompt builder used for the generations
        :param hgen_args: The arguments for the hierarchy generator
        :param task_prompt: The questionnaire prompt given to the model to produce the generations
        :param base_prompt: The main prompt that starts the prompt
        :param summary_prompt: Instructions for the model to create a summary of the system first
        :param artifact_type: The type of artifact being presented in the prompt
        :param combine_summary_and_task_prompts: If True combines the summary and task prompts into a single Questionnaire prompt
        :param build_method: The method to use to build the artifacts into the prompt
        :param id_to_context_artifacts: An optional mapping of artifact id to a list of the related artifacts for context
        :return: The prompt builder used for the generations
        """
        if isinstance(base_prompt, SupportedPrompts):
            base_prompt = base_prompt.value

        generation_step_response_manager = task_prompt.question_prompts[-1].response_manager if isinstance(task_prompt,
                                                                                                           QuestionnairePrompt) \
            else task_prompt.response_manager
        if generation_step_response_manager.value_formatter is None:
            generation_step_response_manager.value_formatter = lambda tag, val: val.strip().strip(NEW_LINE)

        artifact_type = hgen_args.source_type if not artifact_type else artifact_type
        artifact_prompt_kwargs = dict(prompt_prefix=PromptUtil.as_markdown_header(f"{artifact_type.upper()}S:"),
                                      build_method=build_method,
                                      include_ids=build_method == MultiArtifactPrompt.BuildMethod.XML,
                                      data_type=MultiArtifactPrompt.DataType.ARTIFACT,
                                      xml_tags={
                                          HGenUtil.convert_spaces_to_dashes(artifact_type.lower()): ["id",
                                                                                                     "description"]})
        artifact_prompt = ContextPrompt(id_to_context_artifacts=id_to_context_artifacts, **artifact_prompt_kwargs) \
            if id_to_context_artifacts else MultiArtifactPrompt(**artifact_prompt_kwargs)
        prompts = [base_prompt, artifact_prompt]

        task_preface = f"{NEW_LINE}{PromptUtil.as_markdown_header('TASKS:')}{NEW_LINE}"
        if summary_prompt:
            if combine_summary_and_task_prompts:
                task_prompt = QuestionnairePrompt(question_prompts=[summary_prompt, task_prompt],
                                                  prompt_id=task_prompt.id,
                                                  use_multi_step_task_instructions=True)
            else:
                summary_prompt.value = task_preface + summary_prompt.value
                prompts.append(summary_prompt)
        else:
            task_prompt.value = task_preface + task_prompt.value

        prompts.append(task_prompt)
        prompt_builder = PromptBuilder(prompts)
        prompt_builder.format_prompts_with_var(source_type=hgen_args.source_type, target_type=hgen_args.target_type)
        return prompt_builder

    @staticmethod
    def create_artifact_df_from_generated_artifacts(hgen_args: HGenArgs,
                                                    generation_predictions: Dict[str, Set],
                                                    target_layer_id: str,
                                                    generate_names: bool = True) -> Tuple[ArtifactDataFrame, Dict[str, Set]]:
        """
        Creates a dataframe with new artifacts generated to fill in an upper level of the hierarchy
        :param hgen_args: The arguments for the hierarchy generation
        :param generation_predictions: A dictionary mapping generated artifact content to the predicted links
        :param target_layer_id: The id for the layer with the new generated artifacts
        :param generate_names: If True, generates names for the new artifacts
        :return: The dataframe of generated artifacts and a dictionary mapping the new name to the list of predicted related artifacts
        """
        new_artifact_df = ArtifactDataFrame({ArtifactKeys.ID: [str(i) for i in range(len(generation_predictions))],
                                             ArtifactKeys.CONTENT: list(generation_predictions.keys()),
                                             ArtifactKeys.LAYER_ID: [target_layer_id for _ in generation_predictions]})
        if generate_names:
            try:
                logger.info(f"Creating names for {len(new_artifact_df)} {hgen_args.target_type}\n")
                name_prompt = Prompt(f"Create a title for the {hgen_args.target_type} below. "
                                     f"Titles should be a 3-5 word identifier of the {hgen_args.target_type}. ",
                                     PromptResponseManager(response_tag="title", required_tag_ids=REQUIRE_ALL_TAGS,
                                                           value_formatter=lambda tag, val:
                                                           f"{PromptUtil.strip_new_lines_and_extra_space(val)} "
                                                           f"{HGenUtil.get_initials(hgen_args.target_type)}"))
                artifact_prompt = ArtifactPrompt(include_id=False)
                prompt_builder = PromptBuilder(prompts=[name_prompt, artifact_prompt])
                dataset = PromptDataset(artifact_df=new_artifact_df)
                predictions_path = os.path.join(hgen_args.export_dir,
                                                "artifact_names.json") if hgen_args.export_dir else EMPTY_STRING
                names = HGenUtil.get_predictions(prompt_builder, hgen_args=hgen_args,
                                                 prediction_step=PredictionStep.NAME,
                                                 dataset=dataset, response_prompt_ids=name_prompt.id,
                                                 tags_for_response=name_prompt.response_manager.response_tag,
                                                 return_first=True,
                                                 export_path=predictions_path)
                names = [f"{n}{i + 1}" for i, n in enumerate(names)]
                assert len(names) == len(new_artifact_df.index), "Number of predicted names does not match number of artifacts"
                new_artifact_df.index = names
            except Exception:
                logger.exception("Unable to generate names for the artifacts")
        name_2_related_children = {name: links for name, links in
                                   zip(new_artifact_df.index, list(generation_predictions.values()))}
        return new_artifact_df, name_2_related_children

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
    def convert_spaces_to_dashes(str2convert) -> str:
        """
        Converts the str to use dashes instead of spaces
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
        return ''.join(first_letters).upper()
