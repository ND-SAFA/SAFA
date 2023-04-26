from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.abstract_prompt_creator import AbstractPromptCreator
from tgen.testres.base_tests.base_test import BaseTest


class BasePromptTest(BaseTest):

    def verify_prompt(self, generated_prompt):
        self.assertIn("target1", generated_prompt[PromptKeys.PROMPT])
        self.assertTrue(generated_prompt[PromptKeys.PROMPT].endswith(AbstractPromptCreator._PROMPT_SEPARATOR))
        self.assertTrue(generated_prompt[PromptKeys.COMPLETION].startswith(AbstractPromptCreator.COMPLETION_START))
        self.assertTrue(generated_prompt[PromptKeys.COMPLETION].endswith(AbstractPromptCreator._COMPLETION_SEPARATOR))