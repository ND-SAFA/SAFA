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
        return ChatRequest(dataset=dataset, chat_history=chat_history)
