import os
from typing import Dict, Tuple, List

import bs4
from yaml.constructor import SafeConstructor

from tgen.common.constants.path_constants import INPUTS_FOR_GENERATION_PATH
from tgen.common.util.file_util import FileUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.hgen_args import HGenArgs, PredictionStep
from tgen.hgen.hgen_state import HGenState
from tgen.hgen.hgen_util import HGenUtil
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class GenerateInputsStep(AbstractPipelineStep[HGenArgs, HGenState]):

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Creates the input for the generation prompt.
        :param args: HGEN configuration.
        :param state: The current state of the HGEN run.
        :return: None
        """
        state.questions, state.format_of_artifacts, state.description_of_artifact = self._get_inputs(args)

    @staticmethod
    def _get_inputs(hgen_args: HGenArgs) -> Tuple[List, str, str]:
        """
        Gest the inputs that are used to generate the new artifacts
        :param hgen_args: The args for the hgen run
        :return: The inputs that is used to generate the new artifacts (questions, format, description)
        """
        instructions_prompt: Prompt = SupportedPrompts.HGEN_INSTRUCTIONS.value
        instructions_prompt.response_manager.formatter = lambda tag, val: HGenUtil.parse_generated_artifacts(val)
        format_questionnaire: QuestionnairePrompt = SupportedPrompts.HGEN_FORMAT_QUESTIONNAIRE.value

        inputs_response = GenerateInputsStep._get_inputs_response(hgen_args, format_questionnaire, instructions_prompt)
        question_id = instructions_prompt.response_manager.response_tag
        questions = inputs_response[question_id][0]
        artifact_description_tag = format_questionnaire.question_prompts[0].response_manager.response_tag
        artifact_description = inputs_response[artifact_description_tag][0]
        format_of_artifacts = inputs_response[format_questionnaire.question_prompts[-1].response_manager.response_tag][0]

        return questions, format_of_artifacts, artifact_description

    @staticmethod
    def _get_inputs_response(hgen_args: HGenArgs, format_questionnaire: QuestionnairePrompt, summary_questions_prompt: Prompt) -> Dict:
        """
        Gets the inputs used in the prompt of the next step
        :param hgen_args: The arguments for the HGen run
        :param format_questionnaire: The questionnaire prompt to generate format
        :param summary_questions_prompt: The prompt to generate the questions for the summary prompt
        :return: A dictionary mapping input tag to its value
        """

        def construct_tag_from_yaml(loader, node):
            value = loader.construct_scalar(node)
            return bs4.Tag(value)

        input_save_path = GenerateInputsStep._get_inputs_save_path(
            target_type=hgen_args.target_type, source_type=hgen_args.source_type)
        if os.path.exists(input_save_path):
            SafeConstructor.add_constructor('!!python/object:bs4.element.Tag', construct_tag_from_yaml)
            inputs = FileUtil.read_yaml(input_save_path)
        else:
            inputs = GenerateInputsStep._generate_new_inputs(hgen_args, format_questionnaire, summary_questions_prompt)
            FileUtil.write_yaml(inputs, input_save_path)
        return inputs

    @staticmethod
    def _generate_new_inputs(hgen_args: HGenArgs, format_questionnaire: QuestionnairePrompt, summary_questions_prompt: Prompt) -> Dict:
        """
        Asks the model to generate new inputs for the next step
        :param hgen_args: The arguments for the HGen run
        :param format_questionnaire: The questionnaire prompt to generate format
        :param summary_questions_prompt: The prompt to generate the questions for the summary prompt
        :return: The output from the model for the new inputs
        """
        logger.info("Creating new format, description and questions inputs for generation prompt.\n")
        if "title" not in hgen_args.target_type.lower():
            format_questionnaire.question_prompts[-1].value += \
                "The format should be for only the body of the {target_type} and should exclude any title. "
        inputs = {}
        for prompt, step in [(format_questionnaire, PredictionStep.FORMAT), (summary_questions_prompt, PredictionStep.INSTRUCTIONS)]:
            prompt_builder = PromptBuilder(prompts=[prompt])
            prompt_builder.format_prompts_with_var(target_type=hgen_args.target_type, source_type=hgen_args.source_type)
            predictions = HGenUtil.get_predictions(prompt_builder, hgen_args=hgen_args, prediction_step=step,
                                                   response_prompt_ids=prompt.id)[0]
            inputs.update(predictions)
        return inputs

    @staticmethod
    def _get_inputs_save_path(target_type: str, source_type: str) -> str:
        """
        Gets the path to the inputs for generation for a given target type
        :param target_type: The target type being generated
        :return: The path to the save the inputs for generation for a given target type
        """
        file_name = f"{HGenUtil.convert_spaces_to_dashes(source_type)}-to-{HGenUtil.convert_spaces_to_dashes(target_type)}"
        return os.path.join(INPUTS_FOR_GENERATION_PATH, f"{file_name}.yaml")
