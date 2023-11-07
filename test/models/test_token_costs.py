from tgen.models.tokens.token_costs import ModelTokenCost, INPUT_TOKENS
from tgen.testres.base_tests.base_test import BaseTest


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

