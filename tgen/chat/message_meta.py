from dataclasses import dataclass, field
from typing import List, Optional, Set, Tuple

from common_resources.tools.util.base_object import BaseObject
from common_resources.tools.util.list_util import ListUtil
from common_resources.llm.abstract_llm_manager import Message, ROLE_KEY


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

    @staticmethod
    def to_langchain_messages(metas: list["MessageMeta"]) -> List[Tuple]:
        """
        Converts a list of metas to a list of messages for the langchain api.
        :param metas: List of message meta objects.
        :return: A list of messages for the langchain api.
        """
        return [(m.message["role"], m.message["content"]) for m in metas]

    @staticmethod
    def get_most_recent_message(metas: list["MessageMeta"], role: str = None) -> Optional[Message]:
        """
        Gets the most recent message from the given role (if provided otherwise just the last message)
        :param metas: List of message meta objects.
        :param role: If provided, will get the most recent message from that role.
        :return: The most recent message from the given role (if provided otherwise just the last message)
        """
        message_index = -1 if role is None else MessageMeta.index_of_last_response_from_role(metas, role)
        return None if message_index is None else ListUtil.safely_get_item(message_index, metas).message

    @staticmethod
    def index_of_last_response_from_role(metas: list["MessageMeta"], role: str) -> int:
        """
        Gets the index of the recent message from the given role.
        :param metas: List of message meta objects.
        :param role: If provided, will get the most recent message from that role.
        :return: The index of the most recent message from the given role.
        """
        for i, meta in reversed(list(enumerate(metas))):
            if meta.message[ROLE_KEY] == role:
                return i

    @staticmethod
    def is_message_from_role(metas: list["MessageMeta"], role: str, message_index: int = -1) -> bool:
        """
        Returns true if the message at the given index is from the expected role.
        :param metas: List of message meta objects.
        :param role: The role that the message is expected to be from.
        :param message_index: The index to check who the message is from (last by default).
        :return: True if the message at the given index is from the expected role else False.
        """
        meta = ListUtil.safely_get_item(message_index, metas)
        return meta.message[ROLE_KEY] == role if meta else False
