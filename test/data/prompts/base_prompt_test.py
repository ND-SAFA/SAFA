from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.args.supported_ai_prompt_args import SupportedAIPromptArgs
from tgen.testres.base_tests.base_test import BaseTest


class BasePromptTest(BaseTest):
    """
    Provides utility testing methods for prompt testing.
    """

    def verify_prompt(self, generated_prompt, ai_args: SupportedAIPromptArgs = SupportedAIPromptArgs.OPENAI) -> None:
        """
        Verifies that generated prompt contains separators and other library specific formatting.
        :param generated_prompt: The generated prompt to check.
        :param ai_args: The prompt arguments for library used.
        :return: None
        """
        prompt_args = ai_args.value
        self.assertIn("target1", generated_prompt[PromptKeys.PROMPT])
        self.assertTrue(generated_prompt[PromptKeys.PROMPT].endswith(prompt_args.prompt_separator))
        self.assertTrue(generated_prompt[PromptKeys.COMPLETION].startswith(prompt_args.completion_start))
        self.assertTrue(generated_prompt[PromptKeys.COMPLETION].endswith(prompt_args.completion_end))
