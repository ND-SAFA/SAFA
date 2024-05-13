from typing import Dict

from tgen.chat.chat_args import ChatArgs
from tgen.common.constants.deliminator_constants import COMMA
from tgen.common.util.prompt_util import PromptUtil
from tgen.contradictions.common_choices import CommonChoices
from tgen.decision_tree.nodes.llm_node import LLMNode
from tgen.prompts.supported_prompts.chat_prompts import INCLUDE_MORE_CONTEXT_PROMPT, ARTIFACT_TYPE_FOR_CONTEXT_PROMPT


def get_context_type_format_vars(_: str, args: ChatArgs) -> Dict:
    """
    Creates the format vars for the context type node.
    :param args: The arguments to chat.
    :param _: Required for API.
    :return: The format vars for the context type node.
    """
    types = args.dataset.artifact_df.get_artifact_types()
    return {"types": PromptUtil.format_options(types, conjunction="and/or")}


class ChatTree:
    CONTEXT_TYPE_NODE = LLMNode(description=ARTIFACT_TYPE_FOR_CONTEXT_PROMPT.value,
                                input_variable_converter=get_context_type_format_vars,
                                response_manager_params={
                                    "value_formatter": lambda tag, value: [v.strip() for v in value.split(COMMA)]},
                                branches=None)
    STARTING_NODE = LLMNode(description=INCLUDE_MORE_CONTEXT_PROMPT.value, branches={CommonChoices.YES: CONTEXT_TYPE_NODE,
                                                                                     CommonChoices.NO: None})
