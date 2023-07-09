import os
from typing import Tuple

import bs4
from yaml.constructor import SafeConstructor

from tgen.constants.path_constants import GENERATION_QUESTIONNAIRE_PROMPTS_PATH
from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_builder import PromptBuilder
from tgen.data.prompts.prompt_response_manager import PromptResponseManager, REQUIRE_ALL_TAGS
from tgen.data.prompts.question_prompt import QuestionPrompt
from tgen.data.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.data.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.hgen_args import HGenArgs, HGenState, SUMMARY_INSTRUCTIONS
from tgen.hgen.hgen_util import _convert_spaces_to_dashes, _get_prompt_builder_for_generation, get_predictions
from tgen.pipeline.ipipeline import iStep
from tgen.util.file_util import FileUtil
from tgen.util.logging.logger_manager import logger


class GenerateArtifactContent(iStep[HGenArgs, HGenState]):
    def run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Creates the content for the new artifacts.
        :param args: HGEN configuration.
        :param state: The current state of the HGEN run.
        :return: None
        """
        logger.info(f"Generating {args.target_type}s\n")
        summary_questionnaire, format_of_artifacts = GenerateArtifactContent.construct_questionnaire(args)

        source_layer_only_dataset = state.source_dataset
        export_path = state.export_path

        args.format_of_artifacts = format_of_artifacts
        state.generation_questionnaire = summary_questionnaire

        task_prompt = Prompt("Then, reverse engineer as many {target_type}s as possible for the {source_type}. "
                             "Each {target_type} should use the following format '{format}'. "
                             "Enclose all {target_type}s in a comma deliminated list. ",
                             response_manager=PromptResponseManager(
                                 response_tag=_convert_spaces_to_dashes(args.target_type))

                             )
        task_prompt.format_value(format=format_of_artifacts)
        prompt_builder = _get_prompt_builder_for_generation(args, task_prompt, summary_prompt=summary_questionnaire)
        summary_tag = summary_questionnaire.response_manager.response_tag
        generated_artifacts_tag = task_prompt.response_manager.response_tag
        generation_predictions = get_predictions(prompt_builder,
                                                 source_layer_only_dataset,
                                                 args.hgen_llm_manager,
                                                 args.artifact_generation_tokens,
                                                 response_prompt_ids={task_prompt.id, summary_questionnaire.id},
                                                 tags_for_response={generated_artifacts_tag, summary_tag},
                                                 return_first=True,
                                                 export_path=os.path.join(export_path, "artifact_gen_response.yaml"))[0]
        generated_artifact_content = generation_predictions[generated_artifacts_tag]
        summary = generation_predictions[summary_tag]

        state.generated_artifact_content = generated_artifact_content
        state.summary = summary

    @staticmethod
    def construct_questionnaire(hgen_args: HGenArgs) -> Tuple[QuestionnairePrompt, str]:
        """
        Constructs a questionnaire prompt that is used to generate the new artifacts
        :return: The questionnaire prompt that is used to generate the new artifacts
        """

        instructions_prompt: Prompt = SupportedPrompts.HGEN_INSTRUCTIONS.value
        format_prompt: Prompt = Prompt("Finally, provide an example of the typical format for a {target_type}. "
                                       "The format should be for only the body of the {target_type} and should exclude any title.",
                                       response_manager=PromptResponseManager(response_tag="format",
                                                                              required_tag_ids=REQUIRE_ALL_TAGS))  # TODO move this
        questionnaire_content = GenerateArtifactContent._get_content_for_summary_prompt(hgen_args, format_prompt, instructions_prompt)
        step_id, _, instructions_id, _ = instructions_prompt.response_manager.get_all_tag_ids()
        steps = questionnaire_content[step_id]
        questions = [QuestionPrompt(step[instructions_id][0]) for i, step in enumerate(steps) if i < len(steps) - 1]
        format_of_artifacts = questionnaire_content[format_prompt.response_manager.response_tag][0]
        response_manager = PromptResponseManager(response_tag="summary")
        questionnaire_prompt = QuestionnairePrompt(question_prompts=questions,
                                                   enumeration_chars=["-"],
                                                   instructions=SUMMARY_INSTRUCTIONS,
                                                   response_manager=response_manager)

        return questionnaire_prompt, format_of_artifacts

    @staticmethod
    def _get_content_for_summary_prompt(hgen_args: HGenArgs, format_prompt: Prompt, instructions_prompt: Prompt):
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

        questionnaire_prompt_path = GenerateArtifactContent._get_path_to_generation_questionnaire_prompt(
            _convert_spaces_to_dashes(hgen_args.target_type))
        if os.path.exists(questionnaire_prompt_path):
            SafeConstructor.add_constructor('!!python/object:bs4.element.Tag', construct_tag_from_yaml)
            questionnaire_content = FileUtil.read_yaml(questionnaire_prompt_path)
        else:
            logger.info("Creating questionnaire prompt for generation\n")
            prompt_builder = PromptBuilder(prompts=[instructions_prompt, format_prompt])
            prompt_builder.format_prompts_with_var(target_type=hgen_args.target_type, source_type=hgen_args.source_type)
            questionnaire_content = get_predictions(prompt_builder, PromptDataset(),
                                                    response_prompt_ids={instructions_prompt.id, format_prompt.id})[0]
            FileUtil.write_yaml(questionnaire_content, questionnaire_prompt_path)
        return questionnaire_content

    @staticmethod
    def _get_path_to_generation_questionnaire_prompt(target_type: str) -> str:
        """
        Gets the path to the generation questionnaire prompts for a given target type
        :param target_type: The target type being generated
        :return: The path to the generation questionnaire prompts for a given target type
        """
        return os.path.join(GENERATION_QUESTIONNAIRE_PROMPTS_PATH, f"{target_type}.yaml")
