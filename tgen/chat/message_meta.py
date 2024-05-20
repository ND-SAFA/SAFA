from dataclasses import dataclass, field
from typing import List, Set

from tgen.common.util.base_object import BaseObject
from tgen.models.llm.abstract_llm_manager import Message


@dataclass
class MessageMeta(BaseObject):
    """
    Contains message and artifact ids in its context.
    """
    message: Message
    artifact_ids: Set[str] = field(default_factory=set)

    @staticmethod
    def to_llm_messages(metas: list["MessageMeta"]) -> List[Message]:
        """
        Converts a list of metas to a list of messages for the llm api.
        :param metas: List of message meta objects.
        :return: A list of messages for the llm api.
        """
        return [m.message for m in metas]
