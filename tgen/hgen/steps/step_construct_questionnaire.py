import os
import string
from typing import Dict, List

import bs4
from yaml.constructor import SafeConstructor

from tgen.constants.deliminator_constants import NEW_LINE
from tgen.constants.path_constants import GENERATION_QUESTIONNAIRE_PROMPTS_PATH
from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_builder import PromptBuilder
from tgen.data.prompts.prompt_response_manager import PromptResponseManager, REQUIRE_ALL_TAGS
from tgen.data.prompts.question_prompt import QuestionPrompt
from tgen.data.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.data.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.hgen_args import GENERATION_INSTRUCTIONS, HGenArgs
from tgen.hgen.hgen_util import get_predictions
from tgen.util.file_util import FileUtil
from tgen.util.logging.logger_manager import logger


def construct_questionnaire(hgen_args: HGenArgs) -> QuestionnairePrompt:
    """
    Constructs a questionnaire prompt that is used to generate the new artifacts
    :return: The questionnaire prompt that is used to generate the new artifacts
    """

    def construct_tag_from_yaml(loader, node):
        value = loader.construct_scalar(node)
        return bs4.Tag(value)

    instructions_prompt: Prompt = SupportedPrompts.HGEN_INSTRUCTIONS.value
    format_prompt: Prompt = Prompt("Finally, provide an example of the typical format for a {target_type}. "
                                   "The format should be for only the body of the {target_type} and should exclude any title.",
                                   response_manager=PromptResponseManager(response_tag="format",
                                                                          required_tag_ids=REQUIRE_ALL_TAGS))

    questionnaire_prompt_path = _get_path_to_generation_questionnaire_prompt(
        _convert_spaces_to_dashes(hgen_args.target_type))
    if os.path.exists(questionnaire_prompt_path):
        SafeConstructor.add_constructor('!!python/object:bs4.element.Tag', construct_tag_from_yaml)
        questionnaire_content = FileUtil.read_yaml(questionnaire_prompt_path)
    else:
        logger.info("Creating questionnaire prompt for generation\n")
        prompt_builder = PromptBuilder(prompts=[instructions_prompt, format_prompt])
        prompt_builder.format_prompts_with_var(target_type=hgen_args.target_type, source_type=hgen_args.source_type)
        questionnaire_content = get_predictions(prompt_builder,
                                                PromptDataset(),
                                                hgen_args.hgen_llm_manager,
                                                response_prompt_ids={instructions_prompt.id, format_prompt.id})[0]
        FileUtil.write_yaml(questionnaire_content, questionnaire_prompt_path)
    questions = _construct_question_prompts_from_output(hgen_args,
                                                        *instructions_prompt.response_manager.get_all_tag_ids(),
                                                        format_prompt.response_manager.response_tag,
                                                        questionnaire_content)
    questionnaire = QuestionnairePrompt(question_prompts=questions,
                                        instructions=GENERATION_INSTRUCTIONS)

    hgen_args.state.questionnaire = questionnaire


def _construct_question_prompts_from_output(hgen_args: HGenArgs, step_id: str, name_id: str, instructions_id: str, deliverable_id: str,
                                            format_id: str, result: Dict) -> List[QuestionPrompt]:
    """
    Constructs the question prompts from the model output
    :param step_id: The id of the tag for the step
    :param name_id: The id of the tag for the step name
    :param instructions_id: The id of the tag for the step id
    :param deliverable_id: The id of the tag for the step deliverable
    :param format_id: The id of the tag for the artifact format
    :param result: The model output
    :return: The list of question prompts created from model output
    """
    steps = result[step_id]
    questions = []
    target_artifact_tag = _convert_spaces_to_dashes(hgen_args.target_type)
    for i, step in enumerate(steps):
        if i == len(steps) - 1:
            response_tag = f"{target_artifact_tag}-drafts"
            response_instructions_format = f"Output a draft of the {hgen_args.target_type}s in a comma-deliminated list enclosed in"
        else:
            response_tag = _convert_spaces_to_dashes(step[name_id][0])
            deliverable = step[deliverable_id][0]
            deliverable = deliverable[:-1] if deliverable[-1] in string.punctuation else deliverable
            response_instructions_format = f"Output {deliverable} enclosed in"
        response_manager = PromptResponseManager(response_tag=response_tag,
                                                 response_instructions_format=response_instructions_format + ' {}')
        question = QuestionPrompt(step[instructions_id][0], response_manager=response_manager)
        questions.append(question)
    response_manager = PromptResponseManager(response_tag=f"{target_artifact_tag}s",
                                             formatter=lambda tag, val: [v for v in val.split(NEW_LINE) if v],
                                             required_tag_ids=REQUIRE_ALL_TAGS)
    questions.append(QuestionPrompt(f"Finally, output the unique set of {hgen_args.target_type}s that describe the system "
                                    f"with minimal overlap in a comma deliminated list using the following format: "
                                    f"\"{result[format_id][0]}\"", response_manager=response_manager))
    return questions


def _get_path_to_generation_questionnaire_prompt(target_type: str) -> str:
    """
    Gets the path to the generation questionnaire prompts for a given target type
    :param target_type: The target type being generated
    :return: The path to the generation questionnaire prompts for a given target type
    """
    return os.path.join(GENERATION_QUESTIONNAIRE_PROMPTS_PATH, f"{target_type}.yaml")


def _convert_spaces_to_dashes(str2convert) -> str:
    """
    Converts the str to use dashes instead of spaces
    :return: The str with dashes instead of spaces
    """
    return "-".join(str2convert.split()).lower()
