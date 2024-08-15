from dataclasses import dataclass, field
from typing import List

from common_resources.llm.abstract_llm_manager import AbstractLLMManager
from common_resources.tools.constants.default_model_managers import get_best_default_llm_manager_long_context
from common_resources.tools.state_management.args import Args
from common_resources.tools.util.dataclass_util import required_field

from tgen.chat.chat_node_ids import ChatNodeIDs
from tgen.chat.message_meta import MessageMeta


@dataclass
class ChatArgs(Args):
    chat_history: List[MessageMeta] = required_field(field_name="chat_history")
    llm_manager: AbstractLLMManager = field(default_factory=get_best_default_llm_manager_long_context)
    max_context: int = None
    root_node_id: str = ChatNodeIDs.INCLUDE_CONTEXT
    chat_id: str = field(init=False, default=None)

    def __post_init__(self) -> None:
        """
        Performs post initialization steps.
        :return: None
        """
        self.chat_id = f"%.50s" % MessageMeta.get_most_recent_message(self.chat_history)["content"]
