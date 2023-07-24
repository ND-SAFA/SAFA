import os
from typing import Tuple

import bs4
from yaml.constructor import SafeConstructor

from tgen.common.util.file_util import FileUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.prompt_util import PromptUtil
from tgen.constants.deliminator_constants import NEW_LINE
from tgen.constants.path_constants import GENERATION_QUESTIONNAIRE_PROMPTS_PATH
from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_builder import PromptBuilder
from tgen.data.prompts.prompt_response_manager import PromptResponseManager
from tgen.data.prompts.question_prompt import QuestionPrompt
from tgen.data.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.data.prompts.supported_prompts.hgen_prompts import SUMMARY_INSTRUCTIONS, TASK_INSTRUCTIONS
from tgen.data.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.hgen_args import HGenArgs, HGenState, PredictionStep
from tgen.hgen.hgen_util import convert_spaces_to_dashes, get_predictions, get_prompt_builder_for_generation, parse_generated_artifacts
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class GenerateArtifactContent(AbstractPipelineStep[HGenArgs, HGenState]):

    def run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Creates the content for the new artifacts.
        :param args: HGEN configuration.
        :param state: The current state of the HGEN run.
        :return: None
        """
        logger.info(f"Generating {args.target_type}s\n")
        summary_questionnaire, format_of_artifacts, description_of_artifact = GenerateArtifactContent.construct_questionnaire(args)

        source_layer_only_dataset = state.source_dataset
        export_path = os.path.join(state.export_path, "artifact_gen_response.yaml") if state.export_path else None

        state.format_of_artifacts = format_of_artifacts
        state.generation_questionnaire = summary_questionnaire
        state.description_of_artifact = description_of_artifact

        task_prompt = Prompt(TASK_INSTRUCTIONS,
                             response_manager=PromptResponseManager(
                                 response_instructions_format=f"Enclose each {args.target_type} in " + "{}",
                                 response_tag=convert_spaces_to_dashes(f"{args.target_type}"))

                             )
        task_prompt.format_value(format=state.format_of_artifacts, description=description_of_artifact)
        prompt_builder = get_prompt_builder_for_generation(args, task_prompt, summary_prompt=summary_questionnaire)
        if args.system_summary:
            overview_of_system_prompt = Prompt(f"{PromptUtil.format_as_markdown('Overview of System:')}"
                                               f"{NEW_LINE}{args.system_summary}")
            prompt_builder.add_prompt(overview_of_system_prompt, 1)
        summary_tag = summary_questionnaire.response_manager.response_tag
        generated_artifacts_tag = task_prompt.response_manager.response_tag
        generation_predictions = get_predictions(prompt_builder,
                                                 source_layer_only_dataset,
                                                 hgen_args=args,
                                                 prediction_step=PredictionStep.GENERATION,
                                                 response_prompt_ids={task_prompt.id, summary_questionnaire.id},
                                                 tags_for_response={generated_artifacts_tag, summary_tag},
                                                 return_first=False,
                                                 export_path=export_path)[0]
        generated_artifact_content = generation_predictions[generated_artifacts_tag]
        summary = generation_predictions[summary_tag][0]

        state.generated_artifact_content = generated_artifact_content
        state.summary = summary

    @staticmethod
    def construct_questionnaire(hgen_args: HGenArgs) -> Tuple[QuestionnairePrompt, str, str]:
        """
        Constructs a questionnaire prompt that is used to generate the new artifacts
        :return: The questionnaire prompt that is used to generate the new artifacts
        """

        instructions_prompt: Prompt = SupportedPrompts.HGEN_INSTRUCTIONS.value
        instructions_prompt.response_manager.formatter = lambda tag, val: parse_generated_artifacts(val)
        format_questionnaire: QuestionnairePrompt = SupportedPrompts.HGEN_FORMAT_QUESTIONNAIRE.value
        questionnaire_content = GenerateArtifactContent._get_content_for_summary_prompt(hgen_args, format_questionnaire,
                                                                                        instructions_prompt)
        question_id = instructions_prompt.response_manager.response_tag
        questions = questionnaire_content[question_id][0]
        question_prompts = [QuestionPrompt(question) for i, question in enumerate(questions)]
        artifact_description_tag = format_questionnaire.question_prompts[0].response_manager.response_tag
        artifact_description = questionnaire_content[artifact_description_tag][0]
        format_of_artifacts = questionnaire_content[format_questionnaire.question_prompts[-1].response_manager.response_tag][0]
        response_manager = PromptResponseManager(response_tag="summary")
        questionnaire_prompt = QuestionnairePrompt(question_prompts=question_prompts,
                                                   enumeration_chars=["-"],
                                                   instructions=SUMMARY_INSTRUCTIONS,
                                                   response_manager=response_manager)

        return questionnaire_prompt, format_of_artifacts, artifact_description

    @staticmethod
    def _get_content_for_summary_prompt(hgen_args: HGenArgs, format_questionnaire: QuestionnairePrompt, instructions_prompt: Prompt):
        """
        Gets the content for the prompt to generate a summary of system
        :param
        :param format_questionnaire: The prompt asking for a format for the artifact to be generated
        :param instructions_prompt: The prompt to get instructions for the summary
        :return: The generated content
        """

        def construct_tag_from_yaml(loader, node):
            value = loader.construct_scalar(node)
            return bs4.Tag(value)

        questionnaire_prompt_path = GenerateArtifactContent._get_path_to_generation_questionnaire_prompt(
            target_type=hgen_args.target_type, source_type=hgen_args.source_type)
        if os.path.exists(questionnaire_prompt_path):
            SafeConstructor.add_constructor('!!python/object:bs4.element.Tag', construct_tag_from_yaml)
            questionnaire_content = FileUtil.read_yaml(questionnaire_prompt_path)
        else:
            logger.info("Creating questionnaire prompt for generation\n")
            if "title" not in hgen_args.target_type.lower():
                format_questionnaire.question_prompts[-1].value += \
                    "The format should be for only the body of the {target_type} and should exclude any title. "

            questionnaire_content = {}
            for prompt, step in [(format_questionnaire, PredictionStep.FORMAT), (instructions_prompt, PredictionStep.INSTRUCTIONS)]:
                prompt_builder = PromptBuilder(prompts=[prompt])
                prompt_builder.format_prompts_with_var(target_type=hgen_args.target_type, source_type=hgen_args.source_type)
                predictions = get_predictions(prompt_builder,
                                              PromptDataset(),
                                              hgen_args=hgen_args,
                                              prediction_step=step,
                                              response_prompt_ids=prompt.id)[0]
                questionnaire_content.update(predictions)
            FileUtil.write_yaml(questionnaire_content, questionnaire_prompt_path)
        return questionnaire_content

    @staticmethod
    def _get_path_to_generation_questionnaire_prompt(target_type: str, source_type: str) -> str:
        """
        Gets the path to the generation questionnaire prompts for a given target type
        :param target_type: The target type being generated
        :return: The path to the generation questionnaire prompts for a given target type
        """
        file_name = f"{convert_spaces_to_dashes(source_type)}-to-{convert_spaces_to_dashes(target_type)}"
        return os.path.join(GENERATION_QUESTIONNAIRE_PROMPTS_PATH, f"{file_name}.yaml")
