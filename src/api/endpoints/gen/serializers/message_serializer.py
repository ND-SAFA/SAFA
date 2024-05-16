from typing import Dict, List, TypedDict, Set

from rest_framework import serializers

from api.constants.api_constants import TEXT_MEDIUM
from api.endpoints.gen.serializers.abstract_serializer import AbstractSerializer
from tgen.chat.message_meta import MessageMeta
from tgen.models.llm.abstract_llm_manager import Message, PromptRoles


class MessageDTO(TypedDict):
    artifact_ids: Set[str]
    role: str
    content: str


class MessageMetaSerializer(AbstractSerializer):
    content = serializers.CharField(help_text="The content of the message given to the LLM.", required=True)
    role = serializers.CharField(help_text="The author of the content (i.e. user or assistant).", max_length=TEXT_MEDIUM,
                                 required=True)
    artifact_ids = serializers.ListField(help_text="The artifact ids used in the context of the message.",
                                         required=True,
                                         allow_null=False,
                                         allow_empty=True,
                                         child=serializers.CharField(help_text="ID of artifact.", allow_null=False, allow_blank=False)
                                         )

    def create(self, validated_data: Dict) -> MessageMeta:
        """
        Creates message meta containing message and artifact ids.
        :param validated_data: Data after validation.
        :return: MessageMeta
        """
        content = validated_data["content"]
        role = validated_data["role"]
        assert role.upper() in dir(PromptRoles), f"Unknown role: {role}"
        message = Message(content=content, role=role)

        return MessageMeta(message=message, artifact_ids=set(validated_data.get("artifact_ids", set())))
