import mock

from common_resources.llm.tokens.token_calculator import TokenCalculator
from common_resources.llm.tokens.token_costs import ModelTokenCost, INPUT_TOKENS
from common_resources_test.base_tests.base_test import BaseTest


class TestTokenCosts(BaseTest):
    MODEL_NAME = "claude-instant-1.2"
    EXPECTED_COSTS = (0.00163, 0.00551)

    def test_find_token_cost_for_model(self):
        token_cost = ModelTokenCost.find_token_cost_for_model(self.MODEL_NAME)
        self.assertEqual(self.EXPECTED_COSTS, token_cost)

    def test_calculate_cost_for_tokens(self):
        input_cost = ModelTokenCost.calculate_cost_for_tokens(2000, self.MODEL_NAME, input_or_output=INPUT_TOKENS)
        expected_input_cost = self.EXPECTED_COSTS[0] * 2
        self.assertEqual(expected_input_cost, input_cost)

        output_cost = ModelTokenCost.calculate_cost_for_tokens(500, self.MODEL_NAME, input_or_output=INPUT_TOKENS)
        expected_output_cost = self.EXPECTED_COSTS[0] * .5
        self.assertEqual(expected_output_cost, output_cost)

    @mock.patch.object(TokenCalculator, "calculate_max_prompt_tokens")
    def test_truncate_to_fit_tokens(self, max_tokens_mock):
        max_tokens = 10
        max_tokens_mock.return_value = max_tokens
        long_text = "ahhhhhhhhhhhhhhhhhh"
        original_length = TokenCalculator.estimate_num_tokens(long_text)
        truncated = TokenCalculator.truncate_to_fit_tokens(long_text)
        truncated_length = TokenCalculator.estimate_num_tokens(truncated)
        self.assertLess(truncated_length, original_length)
        self.assertLess(truncated_length, max_tokens)
