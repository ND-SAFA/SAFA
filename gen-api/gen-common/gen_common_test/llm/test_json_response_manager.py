import json

from gen_common.llm.anthropic_manager import AnthropicManager
from gen_common.llm.llm_trainer import LLMTrainer
from gen_common.llm.prompts.prompt import Prompt
from gen_common.llm.prompts.prompt_builder import PromptBuilder
from gen_common.llm.response_managers.json_response_manager import JSONResponseManager
from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.tests.base_test import BaseTest


class TestJsonResponseManager(BaseTest):
    @mock_anthropic
    def test_parse_all(self, ai_manager: TestAIManager):
        """
        Tests that parse_all flag to response manager will parse entire response.
        """
        test_obj = {"hi": "hello"}
        ai_manager.add_responses([json.dumps(test_obj)])

        # Step - Make prompt completion.
        prompt = Prompt("SOme Prompt", response_manager=JSONResponseManager(parse_all=True))
        builder = PromptBuilder(prompts=[prompt])
        predictions = LLMTrainer.predict_from_prompts(AnthropicManager(), prompt_builders=[builder])

        # Verify that prompt was completed and prediction created.s
        self.assertSize(1, predictions.predictions)
        prediction = predictions.predictions[0]
        self.assertIn(prompt.args.prompt_id, prediction)
        parsed_output = prediction[prompt.args.prompt_id]

        # Verify that parsed output matched expected
        expected_obj = {k: [v] for k, v in test_obj.items()}  # response manager puts all values in list in case there is more than one
        self.assertEqual(expected_obj, parsed_output)
