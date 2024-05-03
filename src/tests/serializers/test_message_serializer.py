from api.endpoints.gen.hgen.hgen_serializer import HGenRequest, HGenSerializer
from api.endpoints.gen.serializers.message_serializer import MessageSerializer
from tests.base_test import BaseTest
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.testres.test_assertions import TestAssertions


class TestChatSerializer(BaseTest):
    good_data = {
        "messages": [{
            "role": "user",
            "content": "This is the content of the chat."
        },
            {
                "role": "assistant",
                "content": "This is the response of the model."
            }
        ]
    }

    bad_data = {"messages": [{
            "role": "unknown",
            "content": "This is the content of the chat."
        }
        ]}

    def test_positive_serialization(self):
        message_serializer = MessageSerializer(data=self.good_data['messages'], many=True)
        message_serializer.is_valid(raise_exception=True)
        chat_history = message_serializer.save()
        self.assertEqual(len(chat_history), len(chat_history))
        for i, message in enumerate(chat_history):
            self.assertEqual(message["role"], self.good_data["messages"][i]["role"])
            self.assertEqual(message["content"], self.good_data["messages"][i]["content"])

    def test_negative_serialization(self):
        try:
            message_serializer = MessageSerializer(data=self.bad_data['messages'], many=True)
            message_serializer.is_valid(raise_exception=True)
            chat_history = message_serializer.save()
        except AssertionError:
            return

        self.fail("Should fail on unknown role")
