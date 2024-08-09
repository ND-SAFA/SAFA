from common_resources.mocking.library_formatters import anthropic_response_formatter, openai_response_formatter

library_mock_map = {
    "openai": "openai.ChatCompletion.create",
    "anthropic": "common_resources.mocking.mock_anthropic.MockAnthropicClient.messages.create"
}
library_formatter_map = {
    "openai": openai_response_formatter,
    "anthropic": anthropic_response_formatter
}
