from tgen.testres.testprojects.mocking.library_formatters import openai_response_formatter, anthropic_response_formatter

library_mock_map = {
    "openai": "openai.ChatCompletion.create",
    "anthropic": "tgen.testres.testprojects.mocking.mock_anthropic.MockAnthropicClient"
}
library_formatter_map = {
    "openai": openai_response_formatter,
    "anthropic": anthropic_response_formatter
}
