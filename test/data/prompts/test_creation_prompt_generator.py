from test.data.prompts.base_prompt_test import BasePromptTest
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.base_prompt import BasePrompt
from tgen.data.prompts.generation_prompt_creator import GenerationPromptCreator
from tgen.util.override import overrides


class TestClassificationPromptGenerater(BasePromptTest):

    def test_generate(self):
        prompt_creator = GenerationPromptCreator(BasePrompt.SYSTEM_REQUIREMENT_CREATION)

        # No Label
        generated_prompt = prompt_creator.create("source1", "target1")
        self.verify_prompt(generated_prompt)

    @overrides(BasePromptTest)
    def verify_prompt(self, generated_prompt):
        self.assertIn("source1", generated_prompt[PromptKeys.COMPLETION])
        self.assertTrue(generated_prompt[PromptKeys.PROMPT].startswith(BasePrompt.SYSTEM_REQUIREMENT_CREATION.value.split("{}")[0]))
        super().verify_prompt(generated_prompt)
