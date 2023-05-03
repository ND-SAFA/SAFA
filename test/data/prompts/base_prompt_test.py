from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.prompt_args import PromptArgs
from tgen.testres.base_tests.base_test import BaseTest


class BasePromptTest(BaseTest):
    """
    Provides utility testing methods for prompt testing.
    """

    def verify_prompt(self, generated_prompt, prompt_args: PromptArgs) -> None:
        """
        Verifies that generated prompt contains separators and other library specific formatting.
        :param generated_prompt: The generated prompt to check.
        :param prompt_args: The prompt arguments for library used.
        :return: None
        """
        self.assertIn("target1", generated_prompt[PromptKeys.PROMPT])
        self.assertTrue(generated_prompt[PromptKeys.PROMPT].endswith(prompt_args.prompt_suffix))
        self.assertTrue(generated_prompt[PromptKeys.COMPLETION].startswith(prompt_args.completion_prefix))
        self.assertTrue(generated_prompt[PromptKeys.COMPLETION].endswith(prompt_args.completion_suffix))
