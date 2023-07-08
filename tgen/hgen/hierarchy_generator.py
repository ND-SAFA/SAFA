import os
import re
import uuid
from typing import Any, List, Tuple

import bs4
from yaml.constructor import SafeConstructor

from tgen.constants.deliminator_constants import EMPTY_STRING
from tgen.data.clustering.llm_clustering import LLMClustering
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerDataFrame, LayerKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.prompts.prompt_builder import PromptBuilder
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_util import save_dataset_checkpoint
from tgen.hgen.steps.step_construct_questionnaire import construct_questionnaire
from tgen.hgen.steps.step_create_dataset import create_hgen_dataset
from tgen.hgen.steps.step_generate_artifact_content import generate_artifact_content
from tgen.hgen.steps.step_refine_output import refine_artifact_content
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.token_limits import ModelTokenLimits
from tgen.train.trainers.abstract_trainer import AbstractTrainer
from tgen.util.base_object import BaseObject
from tgen.util.dataframe_util import DataFrameUtil
from tgen.util.file_util import FileUtil


class HierarchyGenerator(BaseObject):
    """
    Responsible for generating higher-level artifacts from low-level artifacts
    """
    SUMMARY_INSTRUCTIONS = "First, write a in-depth, comprehensive summary " \
                           "describing the system by focusing on the high level features the system provides its users. " \
                           "Consider the following in your response: "
    RES_TOKENS_MIN = 25000

    def __init__(self, args: HGenArgs):
        """
        Initializes the generator with necessary trainer information
        :param args: The arguments required for the hierarchy generation
        """
        self.args = args
        self._set_max_tokens(self.args.hgen_llm_manager)

    def run(self) -> TraceDataset:
        """
        Runs the hierarchy generator to create a new trace dataset containing generated higher-level artifacts
        :return: Path to exported dataset of generated artifacts
        """
        export_path = os.path.join(self.args.export_dir, str(uuid.uuid4())) if self.args.export_dir else None
        original_dataset_complete, source_layer_only_dataset = self._get_source_datasets_for_generation(export_path)

        self.args.state.export_path = export_path
        self.args.state.source_dataset = source_layer_only_dataset
        self.args.state.original_dataset = original_dataset_complete

        pipeline = [construct_questionnaire,
                    generate_artifact_content,
                    refine_artifact_content,
                    create_hgen_dataset]
        for step in pipeline:
            step(hgen_args=self.args)

        dataset = self.args.state.dataset
        assert dataset is not None, f"Final dataset is not set."
        return dataset

    def _construct_questionnaire_for_generation(self) -> Tuple[QuestionnairePrompt, str]:
        """
        Constructs a questionnaire prompt that is used to generate the new artifacts
        :return: The questionnaire prompt that is used to generate the new artifacts
        """

        instructions_prompt: Prompt = SupportedPrompts.HGEN_INSTRUCTIONS.value
        format_prompt: Prompt = Prompt("Finally, provide an example of the typical format for a {target_type}. "
                                       "The format should be for only the body of the {target_type} and should exclude any title.",
                                       response_manager=PromptResponseManager(response_tag="format",
                                                                              required_tag_ids=REQUIRE_ALL_TAGS))  # TODO move this
        questionnaire_content = self._get_content_for_summary_prompt(format_prompt, instructions_prompt)
        step_id, _, instructions_id, _ = instructions_prompt.response_manager.get_all_tag_ids()
        steps = questionnaire_content[step_id]
        questions = [QuestionPrompt(step[instructions_id][0]) for i, step in enumerate(steps) if i < len(steps) - 1]
        format_of_artifacts = questionnaire_content[format_prompt.response_manager.response_tag][0]
        response_manager = PromptResponseManager(response_tag="summary")
        return QuestionnairePrompt(question_prompts=questions,
                                   enumeration_chars=["-"],
                                   instructions=self.SUMMARY_INSTRUCTIONS,
                                   response_manager=response_manager), format_of_artifacts

    def _get_content_for_summary_prompt(self, format_prompt: Prompt, instructions_prompt: Prompt):
        """
        Gets the content for the prompt to generate a summary of system
        :param
        :param format_prompt: The prompt asking for a format for the artifact to be generated
        :param instructions_prompt: The prompt to get instructions for the summary
        :return: The generated content
        """

        def construct_tag_from_yaml(loader, node):
            value = loader.construct_scalar(node)
            return bs4.Tag(value)

        questionnaire_prompt_path = self._get_path_to_generation_questionnaire_prompt(
            self._convert_spaces_to_dashes(self.args.target_type))
        if os.path.exists(questionnaire_prompt_path):
            SafeConstructor.add_constructor('!!python/object:bs4.element.Tag', construct_tag_from_yaml)
            questionnaire_content = FileUtil.read_yaml(questionnaire_prompt_path)
        else:
            logger.info("Creating questionnaire prompt for generation\n")
            prompt_builder = PromptBuilder(prompts=[instructions_prompt, format_prompt])
            prompt_builder.format_prompts_with_var(target_type=self.args.target_type, source_type=self.args.source_type)
            questionnaire_content = self._get_predictions(prompt_builder, PromptDataset(),
                                                          response_prompt_ids={instructions_prompt.id, format_prompt.id})[0]
            FileUtil.write_yaml(questionnaire_content, questionnaire_prompt_path)
        return questionnaire_content

    def _generate_artifact_content(self, source_layer_only_dataset: PromptDataset, summary_questionnaire: QuestionnairePrompt,
                                   format_of_artifacts: str, export_path: str) -> Tuple[List[str], str]:
        """
        Creates the content for the new artifacts
        :param source_layer_only_dataset: The dataset containing only the source layer
        :param export_path: The path to export predictions to
        :return: The generated artifact content
        """
        logger.info(f"Generating {self.args.target_type}s\n")
        task_prompt = Prompt("Then, reverse engineer as many {target_type}s as possible for the {source_type}. "
                             "Each {target_type} should use the following format '{format}'. "
                             "Enclose all {target_type}s in a comma deliminated list. ",
                             response_manager=PromptResponseManager(
                                 response_tag=self._convert_spaces_to_dashes(self.args.target_type))

                             )
        task_prompt.format_value(format=format_of_artifacts)
        prompt_builder = self._get_prompt_builder_for_generation(task_prompt, summary_prompt=summary_questionnaire)
        summary_tag = summary_questionnaire.response_manager.response_tag
        generated_artifacts_tag = task_prompt.response_manager.response_tag
        generation_predictions = self._get_predictions(prompt_builder, source_layer_only_dataset,
                                                       response_prompt_ids={task_prompt.id, summary_questionnaire.id},
                                                       tags_for_response={generated_artifacts_tag, summary_tag},
                                                       return_first=True,
                                                       export_path=os.path.join(export_path, "artifact_gen_response.yaml"))[0]
        generated_artifact_content = generation_predictions[generated_artifacts_tag]
        summary = generation_predictions[summary_tag]
        return generated_artifact_content, summary

    def _refine_generations(self, generated_artifact_content: List[str], summary: str, questionnaire: QuestionnairePrompt,
                            export_path: str = None, attempt_no: int = 1) -> List[str]:
        """
        Has the model refine the artifact generations
        :param generated_artifact_content: The original generated content
        :param summary: The summary of the dataset
        :param export_path: The path to export predictions to
        :return: A list of refined artifact content
        """
        try:
            logger.info(f"Refining {len(generated_artifact_content)} {self.args.target_type}s\n")
            prompt_builder = self._get_prompt_builder_for_generation(questionnaire,
                                                                     SupportedPrompts.HGEN_REFINE_PROMPT_CONTEXT,
                                                                     artifact_type=self.args.target_type)
            prompt_builder.add_prompt(Prompt(f"{NEW_LINE}{self._format_as_markdown('SUMMARY OF SYSTEM')}: {summary}"), 1)
            artifacts = self._create_artifact_df_with_generated_artifacts(artifact_generations=generated_artifact_content,
                                                                          target_layer_id=self.args.target_type,
                                                                          generate_names=False)
            generated_artifacts_tag = questionnaire.question_prompts[-1].response_manager.response_tag
            refined_artifact_content = self._get_predictions(prompt_builder,
                                                             PromptDataset(artifact_df=artifacts),
                                                             response_prompt_ids=questionnaire.id,
                                                             tags_for_response=generated_artifacts_tag,
                                                             return_first=True,
                                                             export_path=os.path.join(export_path,
                                                                                      f"gen_refinement_response{attempt_no}.yaml"))[0]
        except Exception:
            logger.exception("Refining the artifact content failed. Using original content instead.")
            refined_artifact_content = generated_artifact_content
        return refined_artifact_content

    @staticmethod
    def _convert_spaces_to_dashes(str2convert) -> str:
        """
        Converts the str to use dashes instead of spaces
        :return: The str with dashes instead of spaces
        """
        return "-".join(str2convert.split()).lower()

    @staticmethod
    def _format_generated_artifact_content_from_response(res: str) -> List[str]:
        """
        Formats the generated artifact content from the model response into a list of the artifact content
        :param res: The response from the model containing the generated artifact content
        :return: The list of the generated artifact content
        """
        return [re.sub(r'^\d+\.\s', '', content).strip() for content in res.split(NEW_LINE) if content]

    def _get_target_layer_id(self, original_dataset_complete: PromptDataset) -> str:
        """
        Gets the id of the new target layer
        :param original_dataset_complete: The dataset containing source artifacts
        :return: The id of the new target layer
        """
        layer_id = self.args.target_type
        if self.args.target_type in original_dataset_complete.artifact_df[ArtifactKeys.LAYER_ID].values:
            layer_id = f"{layer_id}_{uuid.uuid4()}"
        return layer_id

    def _get_source_datasets_for_generation(self, export_path: str = EMPTY_STRING) -> Tuple[PromptDataset, PromptDataset]:
        """
        Gets the original source datasets used for the generation
        :param export_path: The path to export checkpoints to
        :return: The original dataset and a dataset with only the source layer
        """
        original_dataset_complete = self.args.dataset_creator_for_sources.create() if self.args.dataset_for_sources is None \
            else self.args.dataset_for_sources
        save_dataset_checkpoint(original_dataset_complete, export_path, filename="initial_dataset_with_sources")
        source_layer_only_dataset = self._create_dataset_with_single_layer(original_dataset_complete.artifact_df,
                                                                           self.args.source_layer_id,
                                                                           original_dataset_complete.trace_dataset.trace_df
                                                                           if original_dataset_complete.trace_dataset else None)
        return original_dataset_complete, source_layer_only_dataset

    @staticmethod
    def _create_dataset_with_single_layer(original_artifact_df: ArtifactDataFrame, layer_id: Any,
                                          original_trace_df: TraceDataFrame = None) -> PromptDataset:
        """
        Creates a trace dataset for a single layer
        :param original_artifact_df: A dataframe containing artifacts including those for the layer
        :param layer_id: ID of the layer to construct a dataset for
        :param original_trace_df: A dataframe containing intra layer traces for the layer
        :return: The trace dataset
        """
        layer_artifact_df = original_artifact_df.filter_by_row(lambda row: row[ArtifactKeys.LAYER_ID.value] == layer_id)
        if len(layer_artifact_df) == 0:
            raise NameError(f"source_layer_id: {layer_id} does not match any artifacts in the dataset")
        layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: [layer_id],
                                   LayerKeys.TARGET_TYPE: [layer_id]})
        layer_trace_df = TraceDataFrame() if original_trace_df is None else \
            TraceDataFrame(DataFrameUtil.filter_df_by_row(original_trace_df,
                                                          lambda row: row[TraceKeys.SOURCE.value] in layer_artifact_df
                                                                      and row[TraceKeys.TARGET.value] in layer_artifact_df))
        trace_df = TraceDatasetCreator.generate_negative_links(artifact_df=layer_artifact_df, trace_df=layer_trace_df,
                                                               layer_mapping_df=layer_df)
        return PromptDataset(trace_dataset=TraceDataset(artifact_df=layer_artifact_df, trace_df=trace_df, layer_df=layer_df))

    @staticmethod
    def _update_trainer_args(trainer: AbstractTrainer, export_path: str) -> None:
        """
        Sets the output directory of the trainer's args to the export path
        :param trainer: The trainer to update output dir for
        :param export_path: The path to set the output dir to
        :return: None
        """
        if hasattr(trainer.trainer_args, "output_dir") and trainer.trainer_args.output_dir is None:
            trainer.trainer_args.output_dir = export_path
        if hasattr(trainer.trainer_args, "metrics"):
            trainer.trainer_args.metrics = []

    @staticmethod
    def _set_max_tokens(llm_manager: AbstractLLMManager) -> int:
        """
        Tries to find the optimal number of tokens to set for the model's response
        :param llm_manager: The LLM Manager being used for the clustering
        :return: The max tokens that the model was set to
        """
        model_token_limit = ModelTokenLimits.get_token_limit_for_model(llm_manager.llm_args.model)
        max_tokens = max(HierarchyGenerator.RES_TOKENS_MIN, int(model_token_limit * LLMClustering.PERC_TOKENS_FOR_RES))
        llm_manager.llm_args.set_max_tokens(max_tokens)
        return max_tokens

    @staticmethod
