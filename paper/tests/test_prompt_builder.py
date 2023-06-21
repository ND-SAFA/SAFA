from unittest import TestCase

from paper.common.prompt_builder import PromptBuilder


class TestPromptBuilder(TestCase):
    def test_basic(self):
        builder = PromptBuilder()
        builder.with_artifact("RE-8", "First artifact body.").with_task("Summarize this artifact.").with_body_title(None)
        prompt = builder.get()
        print(prompt)
