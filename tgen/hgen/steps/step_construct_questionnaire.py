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
from tgen.hgen.hgen_args import HGenArgs, SUMMARY_INSTRUCTIONS
from tgen.hgen.hgen_util import _convert_spaces_to_dashes, get_predictions
from tgen.util.file_util import FileUtil
from tgen.util.logging.logger_manager import logger


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
    questionnaire_content = _get_content_for_summary_prompt(hgen_args, format_prompt, instructions_prompt)
    step_id, _, instructions_id, _ = instructions_prompt.response_manager.get_all_tag_ids()
    steps = questionnaire_content[step_id]
    questions = [QuestionPrompt(step[instructions_id][0]) for i, step in enumerate(steps) if i < len(steps) - 1]
    hgen_args.format_of_artifacts = questionnaire_content[format_prompt.response_manager.response_tag][0]
    response_manager = PromptResponseManager(response_tag="summary")
    hgen_args.state.generation_questionnaire = QuestionnairePrompt(question_prompts=questions,
                                                                   enumeration_chars=["-"],
                                                                   instructions=SUMMARY_INSTRUCTIONS,
                                                                   response_manager=response_manager)


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

    questionnaire_prompt_path = _get_path_to_generation_questionnaire_prompt(
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


def _get_path_to_generation_questionnaire_prompt(target_type: str) -> str:
    """
    Gets the path to the generation questionnaire prompts for a given target type
    :param target_type: The target type being generated
    :return: The path to the generation questionnaire prompts for a given target type
    """
    return os.path.join(GENERATION_QUESTIONNAIRE_PROMPTS_PATH, f"{target_type}.yaml")
