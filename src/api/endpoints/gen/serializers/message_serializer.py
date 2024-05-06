from typing import Dict

from rest_framework import serializers

from api.constants.api_constants import TEXT_MEDIUM
from api.endpoints.gen.chat.chat_serializer import MessageMeta
from api.endpoints.gen.serializers.abstract_serializer import AbstractSerializer
from tgen.common.objects.artifact import Artifact
from tgen.models.llm.abstract_llm_manager import Message, PromptRoles


class MessageSerializer(AbstractSerializer):
    content = serializers.CharField(help_text="The content of the message given to the LLM.", required=True)
    role = serializers.CharField(help_text="The author of the content (i.e. user or assistant).", max_length=TEXT_MEDIUM,
                                 required=True)

    def create(self, validated_data: Dict) -> Artifact:
        """
        Serializes artifact from input data.
        :param validated_data: The JSON for an artifact.
        :return: The artifact.
        """
        content = validated_data["content"]
        role = validated_data["role"]
        assert role.upper() in dir(PromptRoles), f"Unknown role: {role}"
        return Message(content=content, role=role)


class MessageMetaSerializer(AbstractSerializer):
    message = MessageSerializer(help_text="The message containing content and role.", required=True)
    artifact_ids = serializers.ListField(help_text="The artifact ids used in the context of the message.", required=True,
                                         allow_null=False, allow_empty=True)

    def create(self, validated_data: Dict) -> MessageMeta:
        """
        Creates message meta containing message and artifact ids.
        :param validated_data: Data after validation.
        :return: MessageMeta
        """

        message_serializer = MessageSerializer(data=validated_data["message"])
        message_serializer.is_valid(raise_exception=True)
        message = message_serializer.save()

        return MessageMeta(message=message, artifact_ids=validated_data["artifact_ids"])
