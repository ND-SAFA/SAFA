from tgen.common.util.enum_util import EnumDict
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.binary_choice_question_prompt import BinaryChoiceQuestionPrompt
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.question_prompt import QuestionPrompt
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.response_managers.xml_response_manager import XMLResponseManager
from tgen.prompts.select_question_prompt import SelectQuestionPrompt
from tgen.testres.base_tests.base_test import BaseTest


class TestPromptBuilder(BaseTest):
    ARTIFACTS = [EnumDict({ArtifactKeys.ID: "id2",
                           ArtifactKeys.CONTENT: "content2"}),
                 EnumDict({ArtifactKeys.ID: "id3",
                           ArtifactKeys.CONTENT: "content3"})
                 ]
    ARTIFACT = EnumDict({ArtifactKeys.ID: "id1",
                         ArtifactKeys.CONTENT: "content1"})

    def test_format_vars(self):
        prompt_builder = self.get_prompt_builder()
        fill_ins = ["animal", "sport", "book"]
        prompt_builder.format_variables = {"blank": fill_ins}
        prompt1 = prompt_builder.build(AnthropicManager.prompt_args, artifacts=self.ARTIFACTS, artifact=self.ARTIFACT)
        prompt2 = prompt_builder.build(AnthropicManager.prompt_args, artifacts=self.ARTIFACTS, artifact=self.ARTIFACT)
        prompt3 = prompt_builder.build(AnthropicManager.prompt_args, artifacts=self.ARTIFACTS, artifact=self.ARTIFACT)
        for i, prompt_dict in enumerate([prompt1, prompt2, prompt3]):
            prompt = prompt_dict[PromptKeys.PROMPT]
            for j, fill_in in enumerate(fill_ins):
                if i == j:
                    self.assertIn(fill_in, prompt)
                else:
                    self.assertNotIn(fill_in, prompt)
        prompt4 = prompt_builder.build(AnthropicManager.prompt_args, artifacts=self.ARTIFACTS, artifact=self.ARTIFACT)
        self.assertIn("{blank}", prompt4[PromptKeys.PROMPT])

    def test_build(self):
        prompt_builder = self.get_prompt_builder()
        prompt_dict = prompt_builder.build(AnthropicManager.prompt_args, artifact=self.ARTIFACT,
                                           artifacts=self.ARTIFACTS,
                                           correct_completion="yes", blank="cat")
        self.assertIn("answer with the following", prompt_dict[PromptKeys.PROMPT])
        self.assertIn("Think about your favorite", prompt_dict[PromptKeys.PROMPT])
        self.assertIn("Apple", prompt_dict[PromptKeys.PROMPT])
        self.assertIn("Banana", prompt_dict[PromptKeys.PROMPT])
        self.assertIn("Cat", prompt_dict[PromptKeys.PROMPT])
        self.assertIn("content1", prompt_dict[PromptKeys.PROMPT])
        self.assertIn("content2", prompt_dict[PromptKeys.PROMPT])
        self.assertIn("content3", prompt_dict[PromptKeys.PROMPT])
        self.assertIn("yes", prompt_dict[PromptKeys.COMPLETION])

    def test_parse_response(self):
        prompt_builder = self.get_prompt_builder()
        output = prompt_builder.parse_responses("<question2>test</question2><choice>yes</choice><category>A</category>")
        for prompt in prompt_builder.get_all_prompts():
            self.assertIn(prompt.args.prompt_id, output)
            if isinstance(prompt, BinaryChoiceQuestionPrompt):
                self.assertEqual(output[prompt.args.prompt_id]["choice"][0], "yes")
            elif isinstance(prompt, QuestionnairePrompt):
                self.assertEqual(output[prompt.args.prompt_id]["question2"][0], "test")
            elif isinstance(prompt, SelectQuestionPrompt):
                self.assertEqual(output[prompt.args.prompt_id]["category"][0], "A")

    def test_create_config(self):
        prompt_builder = self.get_prompt_builder()
        self.assertTrue(prompt_builder.config.requires_trace_per_prompt)
        self.assertTrue(prompt_builder.config.requires_artifact_per_prompt)
        self.assertFalse(prompt_builder.config.requires_all_artifacts)

        prompt_builder = self.get_prompt_builder(data_type=MultiArtifactPrompt.DataType.ARTIFACT)
        self.assertFalse(prompt_builder.config.requires_trace_per_prompt)
        self.assertTrue(prompt_builder.config.requires_artifact_per_prompt)
        self.assertTrue(prompt_builder.config.requires_all_artifacts)

    def get_prompt_builder(self, data_type=MultiArtifactPrompt.DataType.TRACES):
        prompts = [ArtifactPrompt(),
                   BinaryChoiceQuestionPrompt(["yes", "no"], "answer with the following:"),
                   MultiArtifactPrompt(data_type=data_type),
                   QuestionnairePrompt(instructions="Answer all of the following",
                                       enumeration_chars=["i", "ii", "iii"],
                                       question_prompts={
                                           1: QuestionPrompt("Think about your favorite {blank}"),
                                           2: QuestionPrompt("Then do this",
                                                             response_manager=XMLResponseManager(response_tag="question2")),
                                           3: BinaryChoiceQuestionPrompt(choices=["yes", "no"], question="Do you like running?")

                                       }),
                   SelectQuestionPrompt({1: "Apple", 2: "Banana", 3: "Cat"})
                   ]
        return PromptBuilder(prompts)
