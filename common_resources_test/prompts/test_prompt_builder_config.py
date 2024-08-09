from typing import List, Union

from common_resources.tools.util.reflection_util import ReflectionUtil
from common_resources.llm.prompts.artifact_prompt import ArtifactPrompt
from common_resources.llm.prompts.multi_artifact_prompt import MultiArtifactPrompt
from common_resources.llm.prompts.prompt import Prompt
from common_resources.llm.prompts.prompt_builder import PromptBuilder
from common_resources.llm.prompts.question_prompt import QuestionPrompt
from common_resources_test.base_tests.base_test import BaseTest


class TestResponse:
    id = "id_from_res"


class TestPromptBuilderConfig(BaseTest):

    def test_no_prompts(self):
        """
        Verifies that no prompts results in no requirements.
        """
        self.verify_config([])

    def test_question_prompt(self):
        """
        Verifies that no prompts results in no requirements.
        """
        question_prompt = QuestionPrompt("This is a question")
        self.verify_config(question_prompt)

    def test_artifact_prompt(self):
        """
        Verifies that no prompts results in no requirements.
        """
        artifact_prompt = ArtifactPrompt("Please describe this artifact: ")
        self.verify_config(artifact_prompt, "requires_artifact_per_prompt")

    def test_multi_artifact_prompt(self):
        """
        Verifies that multi artifact prompt requires all artifacts.
        """
        multi_artifact_prompt = MultiArtifactPrompt("Please describe this artifact: ")
        self.verify_config(multi_artifact_prompt, "requires_all_artifacts")

    def test_trace_prompt(self):
        """
        Verifies that multi artifact prompt requires all artifacts.
        """
        multi_artifact_prompt = MultiArtifactPrompt("Please describe this artifact: ", data_type=MultiArtifactPrompt.DataType.TRACES)
        self.verify_config(multi_artifact_prompt, ["requires_trace_per_prompt"])

    def test_composite(self):
        question_prompt = QuestionPrompt("This is a question")
        artifact_prompt = ArtifactPrompt("Please describe this artifact: ")
        multi_artifact_prompt = MultiArtifactPrompt("Please describe this artifact: ")
        multi_artifact_prompt_traces = MultiArtifactPrompt("Please describe this artifact: ",
                                                           data_type=MultiArtifactPrompt.DataType.TRACES)
        prompts = [question_prompt, artifact_prompt, multi_artifact_prompt, multi_artifact_prompt_traces]
        self.verify_config(prompts, ["requires_trace_per_prompt", "requires_artifact_per_prompt", "requires_all_artifacts"])

    def verify_config(self, prompts: Union[Prompt, List[Prompt]], true_flags: Union[str, List[str]] = None):
        if isinstance(prompts, Prompt):
            prompts = [prompts]
        if true_flags is None:
            true_flags = []
        if isinstance(true_flags, str):
            true_flags = [true_flags]
        prompt_builder = PromptBuilder(prompts)
        config = prompt_builder.config
        config_fields = ReflectionUtil.get_fields(config)
        for field_name, field_value in config_fields.items():
            assertion = self.assertTrue if field_name in true_flags else self.assertFalse
            assertion(field_value, msg=f"{field_name} received unexpected value.")
