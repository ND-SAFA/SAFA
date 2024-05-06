from dataclasses import dataclass
from typing import List

from tgen.common.util.base_object import BaseObject
from tgen.models.llm.abstract_llm_manager import Message


@dataclass
class MessageMeta(BaseObject):
    """
    Contains message and artifact ids in its context.
    """
    message: Message
    artifact_ids: List[str]
