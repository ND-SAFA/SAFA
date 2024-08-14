from common_resources.tools.constants.symbol_constants import EMPTY_STRING

from tgen.common.constants.concept_pipeline_constants import ENTITY_NAME_TAG, ENTITY_TAG
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_args import PromptArgs
from tgen.prompts.response_managers.xml_response_manager import XMLResponseManager

"""
Entity Extraction
"""


def get_response_format():
    """
    Creates the example response format used in the prompt to the LLM.
    :return: Example of how to format an extracted entity.
    """
    return create_entity_extraction_response("ENTITY", prefix="Record each entity like so: \n")


def create_entity_extraction_response(name: str, prefix: str = EMPTY_STRING) -> str:
    """
    :param name: The entity name.
    :param prefix: Goes before the response tags.
    :return: Expected response format for each entity found.
    """
    return (
        f"{prefix}"
        f"<{ENTITY_TAG}>"
        f"<{ENTITY_NAME_TAG}>{name}</{ENTITY_NAME_TAG}>"
        f"</{ENTITY_TAG}>"
    )


ENTITY_EXTRACTION_PROMPT = Prompt("Above is an artifact from a software system. "
                                  "Please extract the key project-specific entities used in the artifact. "
                                  "Entities include project concepts, acronyms, and terminology "
                                  "that would mostly likely need to be defined in a project glossary. "
                                  ""
                                  "If none exists, just say 'NA'",
                                  prompt_args=PromptArgs(title="Task\n"),
                                  response_manager=XMLResponseManager(
                                      response_tag={ENTITY_TAG: [ENTITY_NAME_TAG, ENTITY_NAME_TAG]},
                                      response_instructions_format=get_response_format()))

"""
Entity Matching
---
*Note, prompts objects cannot live here because many are created per artifact.*
"""
ENTITY_MATCHING_INSTRUCTIONS = "List the artifacts that are cited in the text below. If none exists, just say 'NA'."
ENTITY_MATCHING_RESPONSE_FORMAT = "Record each referenced entity like so {}."
