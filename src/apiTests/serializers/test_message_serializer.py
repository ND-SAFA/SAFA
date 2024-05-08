from typing import List

from api.endpoints.gen.serializers.message_serializer import MessageMetaSerializer
from apiTests.base_test import BaseTest
from tgen.chat.message_meta import MessageMeta


class TestChatSerializer(BaseTest):
    good_data = {
        "messages": [
            {
                "role": "user",
                "content": "This is the content of the chat.",
                "artifact_ids": []
            },
            {
                "role": "assistant",
                "content": "This is the response of the model.",
                "artifact_ids": []
            }
        ]
    }

    bad_data = {"messages": [{
        "role": "unknown",
        "content": "This is the content of the chat.",
        "artifact_ids": []
    }
    ]}

    def test_positive_serialization(self):
        message_serializer = MessageMetaSerializer(data=self.good_data['messages'], many=True)
        message_serializer.is_valid(raise_exception=True)
        chat_history: List[MessageMeta] = message_serializer.save()
        self.assertEqual(len(chat_history), len(chat_history))
        for i, meta in enumerate(chat_history):
            self.assertEqual(meta.message["role"], self.good_data["messages"][i]["role"])
            self.assertEqual(meta.message["content"], self.good_data["messages"][i]["content"])

    def test_negative_serialization(self):
        try:
            message_serializer = MessageMetaSerializer(data=self.bad_data['messages'], many=True)
            message_serializer.is_valid(raise_exception=True)
            chat_history = message_serializer.save()
        except AssertionError:
            return

        self.fail("Should fail on unknown role")
