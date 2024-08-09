from common_resources.tools.util.prompt_util import PromptUtil
from common_resources.llm.prompts.conditional_prompt import ConditionalPrompt
from common_resources.llm.prompts.prompt import Prompt
from common_resources.llm.response_managers.xml_response_manager import XMLResponseManager
from common_resources_test.base_tests.base_test import BaseTest


class TestConditionalPrompt(BaseTest):

    def test_build(self):
        conditional_prompt, prompt1tag, prompt1txt, prompt2tag, prompt2txt = self._get_prompt()
        prompt1 = conditional_prompt.build(indicator=0)
        self.assertIn(prompt1txt, prompt1)
        prompt2 = conditional_prompt.build(indicator="1")
        self.assertIn(prompt2txt, prompt2)
        prompt2 = conditional_prompt.build(indicator=True)
        self.assertIn(prompt2txt, prompt2)
        self.assertFalse(conditional_prompt.build(indicator=2))

    def test_parse_response(self):
        conditional_prompt, prompt1tag, prompt1txt, prompt2tag, prompt2txt = self._get_prompt()
        prompt1res = conditional_prompt.parse_response(PromptUtil.create_xml(prompt1tag, prompt1txt))
        self.assertIn(prompt1tag, prompt1res)
        self.assertEqual(prompt1res[prompt1tag][0], prompt1txt)
        prompt2res = conditional_prompt.parse_response(PromptUtil.create_xml(prompt2tag, prompt2txt))
        self.assertIn(prompt2tag, prompt2res)
        self.assertEqual(prompt2res[prompt2tag][0], prompt2txt)

    def test_format_value(self):
        conditional_prompt, prompt1tag, prompt1txt, prompt2tag, prompt2txt = self._get_prompt()
        variable = "hello"
        conditional_prompt.format_value(var=variable)
        prompt1 = conditional_prompt.build(indicator=0)
        self.assertIn(variable, prompt1)
        prompt2 = conditional_prompt.build(indicator=1)
        self.assertIn(variable, prompt2)

    def _get_prompt(self):
        prompt1txt = "prompt1{var}"
        prompt1tag = "one"
        prompt2txt = "prompt2{var}"
        prompt2tag = "two"
        conditional_prompt = ConditionalPrompt(candidate_prompts=[Prompt(prompt1txt,
                                                                         response_manager=XMLResponseManager(
                                                                             response_tag=prompt1tag)),
                                                                  Prompt(prompt2txt,
                                                                         response_manager=XMLResponseManager(
                                                                             response_tag=prompt2tag))
                                                                  ],
                                               prompt_selector=lambda kwargs: kwargs.get("indicator"))
        return conditional_prompt, prompt1tag, prompt1txt, prompt2tag, prompt2txt
