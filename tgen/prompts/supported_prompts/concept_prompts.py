from tgen.common.constants.concept_pipeline_constants import ENTITY_DESCRIPTION_TAG, ENTITY_NAME_TAG, ENTITY_TAG
from tgen.prompts.prompt import Prompt
from tgen.prompts.prompt_response_manager import PromptResponseManager

"""
Entity Extraction
"""


def get_response_format():
    """
    Creates the example response format used in the prompt to the LLM.
    :return: Example of how to format an extracted entity.
    """
    return create_entity_extraction_response("ACRONYM", "DESCRIPTION", prefix="Record each acronym like so: \n")


def create_entity_extraction_response(name: str, description: str, prefix: str = "") -> str:
    """
    :return: Expected response format for each entity found.
    """
    return (
        f"{prefix}"
        f"<{ENTITY_TAG}>"
        f"<{ENTITY_NAME_TAG}>{name}</{ENTITY_NAME_TAG}>"
        f"<{ENTITY_DESCRIPTION_TAG}>{description}</{ENTITY_DESCRIPTION_TAG}>"
        f"</{ENTITY_TAG}>"
    )


ENTITY_EXTRACTION_PROMPT = Prompt("Above is an artifact from a software system. "
                                  "Please extract the acronyms used in the artifact. "
                                  "Attempt to define each acronym found. ",
                                  title="Instructions\n",
                                  response_manager=PromptResponseManager(
                                      response_tag={ENTITY_TAG: [ENTITY_NAME_TAG, ENTITY_DESCRIPTION_TAG]},
                                      response_instructions_format=get_response_format()))

"""
Entity Matching
---
*Note, prompts objects cannot live here because many are created per artifact.*
"""
ENTITY_MATCHING_INSTRUCTIONS = "List the artifacts that are cited in the text below. If none exists, just say 'NA'."
ENTITY_MATCHING_RESPONSE_FORMAT = "Record each referenced entity like so {}."
