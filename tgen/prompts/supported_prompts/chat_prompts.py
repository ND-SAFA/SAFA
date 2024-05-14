from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.prompts.prompt import Prompt

ALL_TYPES_RESPONSE = "all"

USER_INPUT_STARTER = f"The user would like to you to answer the following about their specific project: {NEW_LINE}" \
                     "query: {user_query}" \
                     f"{NEW_LINE}"

INCLUDE_MORE_CONTEXT_PROMPT = Prompt(USER_INPUT_STARTER +
                                     f"To give them the most specific answer, do you need additional "
                                     "information about their project, more than is already provided in the chat? ")

ARTIFACT_TYPE_FOR_CONTEXT_PROMPT = Prompt(USER_INPUT_STARTER +
                                          "What type of artifact(s) would be most useful for answering the query: "
                                          "{types}? If one or more artifacts would be useful, answer in a comma-deliminated list. "
                                          f"If all artifact types would be useful, respond with '{ALL_TYPES_RESPONSE}'. ",
                                          )
