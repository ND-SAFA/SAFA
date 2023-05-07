from api.endpoints.generation.generation_serializer import GenerationSerializer
from api.tests.api_base_test import ApiBaseTest


class TestGenerationSerializer(ApiBaseTest):
    def test_pos_serialization(self):
        model_name = "davinci"
        prompt = "hello, my name is "
        payload = {
            "model": model_name,
            "prompt": prompt
        }
        serializer = GenerationSerializer(data=payload)
        self.assertTrue(serializer.is_valid())
        data = serializer.save()
        self.assertEqual(model_name, data["model"])
        self.assertEqual(prompt, data["prompt"])
