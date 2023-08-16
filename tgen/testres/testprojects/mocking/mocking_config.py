from tgen.testres.testprojects.mocking.library_formatters import anthropic_response_formatter, openai_response_formatter

library_mock_map = {
    "openai": "openai.ChatCompletion.create",
    "anthropic": "tgen.testres.testprojects.mocking.mock_anthropic.MockAnthropicClient.completion"
}
library_formatter_map = {
    "openai": openai_response_formatter,
    "anthropic": anthropic_response_formatter
}
