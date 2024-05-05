from dataclasses import dataclass
from typing import List

from api.endpoints.gen.serializers.abstract_serializer import AbstractSerializer
from api.endpoints.gen.serializers.dataset_serializer import DatasetSerializer
from api.endpoints.gen.serializers.message_serializer import MessageSerializer
from tgen.common.util.base_object import BaseObject
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.models.llm.abstract_llm_manager import Message


@dataclass
class ChatRequest(BaseObject):
    dataset: ApiDefinition
    chat_history: List[Message]


class ChatSerializer(AbstractSerializer):
    """
    Serializes the request for performing health checks on an artifact.
    """
    dataset = DatasetSerializer(help_text="The dataset used for context.")
    chat_history = MessageSerializer(many=True, help_text="List of messages exchanged with the LLM.")

    def create(self, validated_data) -> ChatRequest:
        """
        Serializes Health Check request.
        :param validated_data: The JSON input data.
        :return: Health Check Request.
        """
        dataset_serializer = DatasetSerializer(data=validated_data["dataset"])
        dataset_serializer.is_valid(raise_exception=True)
        dataset = dataset_serializer.save()
        message_serializer = MessageSerializer(data=validated_data["chat_history"], many=True)
        message_serializer.is_valid(raise_exception=True)
        chat_history = message_serializer.save()
        self._assert_valid_history(chat_history)
        return ChatRequest(dataset=dataset, chat_history=chat_history)

    @staticmethod
    def _assert_valid_history(chat_history: List[Message]):
        """
        Asserts chat history constraints.
        :param chat_history: List of messages in chat.
        :return:
        """
        if len(chat_history) == 0:
            raise ValueError("No messages given to chat.")
        if chat_history[-1]["role"] != "user":
            raise ValueError("Last message must be user message.")

        for i in range(0, len(chat_history) - 1):
            if chat_history[i]["role"] == chat_history[i + 1]["role"]:
                role = chat_history[i]["role"]
                raise ValueError(f"Found two messages with {role} in a row.")
