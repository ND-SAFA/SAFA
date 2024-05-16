from dataclasses import dataclass, field
from typing import List

from tgen.chat.message_meta import MessageMeta
from tgen.common.constants.deliminator_constants import DASH
from tgen.common.constants.model_constants import get_best_default_llm_manager_long_context
from tgen.common.util.dataclass_util import required_field
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager, CONTENT_KEY
from tgen.pipeline.pipeline_args import PipelineArgs


@dataclass
class ChatArgs(PipelineArgs):
    chat_history: List[MessageMeta] = required_field(field_name="chat_history")
    llm_manager: AbstractLLMManager = field(default_factory=get_best_default_llm_manager_long_context)
    max_context: int = None
    chat_id: int = field(init=False, default=None)

    def __post_init__(self) -> None:
        """
        Performs post initialization steps.
        :return: None
        """
        self.chat_id = hash(DASH.join([meta.message[CONTENT_KEY] for meta in self.chat_history]))
