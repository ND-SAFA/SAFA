from dataclasses import dataclass
from typing import List

from tgen.chat.message_meta import MessageMeta
from tgen.common.util.dataclass_util import required_field
from tgen.pipeline.pipeline_args import PipelineArgs


@dataclass
class ChatArgs(PipelineArgs):
    chat_history: List[MessageMeta] = required_field(field_name="chat_history")
    system_prompt: str = None
