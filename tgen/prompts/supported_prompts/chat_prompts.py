from common_resources.tools.constants.symbol_constants import NEW_LINE
from common_resources.tools.util.str_util import StrUtil
from tgen.prompts.prompt import Prompt

ALL_TYPES_RESPONSE = "all"
TYPES_FORMAT_VAR = "types"

USER_INPUT_STARTER = f"The user would like to you to answer the following about their specific project: {NEW_LINE}" \
                     "query: {user_query}" \
                     f"{NEW_LINE}"

INCLUDE_MORE_CONTEXT_PROMPT = Prompt(USER_INPUT_STARTER +
                                     f"To give them the most specific answer, do you need additional "
                                     "information about their project, more than is already provided in the chat? ")

ARTIFACT_TYPE_FOR_CONTEXT_PROMPT = Prompt(USER_INPUT_STARTER +
                                          StrUtil.fill_with_format_variable_name("What type of artifact(s) would be most useful "
                                                                                 "for answering the query: {}?",
                                                                                 TYPES_FORMAT_VAR) +
                                          "If one or more artifacts would be useful, answer in a comma-deliminated list. "
                                          f"If all artifact types would be useful, respond with '{ALL_TYPES_RESPONSE}'. ",
                                          )

REWRITE_QUERY_PROMPT = Prompt(USER_INPUT_STARTER +
                              f"Re-write the query so that it will be easier to identify only the necessary "
                              f"context required to answer. For example, if a user asked 'How does the code "
                              f"ensure that user account access is secure when logging in?' the query might be "
                              f"rewritten to 'Secure account access on login'")
