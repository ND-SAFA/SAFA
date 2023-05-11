from test.data.prompts.base_prompt_test import BasePromptTest
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.classification_prompt_creator import ClassificationPromptCreator
from tgen.data.prompts.supported_prompts import SupportedPrompts
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.util.override import overrides


class TestClassificationPromptGenerater(BasePromptTest):

    def test_generate(self):
        prompt_creator = ClassificationPromptCreator(pos_class="yass", neg_class="nope")

        # No Label
        generated_prompt = prompt_creator.create("target1", "source1")
        self.verify_prompt(generated_prompt)

        generated_prompt = prompt_creator.create("target1", "source1", label=0)
        self.verify_prompt(generated_prompt)
        self.assertIn("nope", generated_prompt[PromptKeys.COMPLETION])

        generated_prompt = prompt_creator.create("target1", "source1", label=1)
        self.verify_prompt(generated_prompt)
        self.assertIn("yass", generated_prompt[PromptKeys.COMPLETION])

    @overrides(BasePromptTest)
    def verify_prompt(self, generated_prompt):
        self.assertIn("source1", generated_prompt[PromptKeys.PROMPT])
        self.assertTrue(generated_prompt[PromptKeys.PROMPT].startswith(SupportedPrompts.CLASSIFICATION.value))
        super().verify_prompt(generated_prompt, OpenAIManager.prompt_args)  # assumed using openai
