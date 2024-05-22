from dataclasses import dataclass, field
from typing import List

from tgen.chat.chat_node_ids import ChatNodeIDs
from tgen.chat.message_meta import MessageMeta
from tgen.common.constants.model_constants import get_best_default_llm_manager_long_context
from tgen.common.util.dataclass_util import required_field
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.pipeline.pipeline_args import PipelineArgs


@dataclass
class ChatArgs(PipelineArgs):
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
