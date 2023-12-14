from api.endpoints.completion.completion_serializer import CompletionSerializer
from tests.base_test import BaseTest


class TestGenerationSerializer(BaseTest):
    def test_pos_serialization(self):
        prompt = "hello, my name is "
        payload = {
            "prompt": prompt
        }
        serializer = CompletionSerializer(data=payload)
        self.assertTrue(serializer.is_valid())
        data = serializer.save()
        self.assertEqual(prompt, data["prompt"])
