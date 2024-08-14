from common_resources.tools.util.enum_util import EnumDict
from common_resources.data.dataframes.prompt_dataframe import PromptDataFrame
from common_resources.data.keys.prompt_keys import PromptKeys
from tgen.testres.base_tests.base_test import BaseTest


class TestPromptDataFrame(BaseTest):

    def test_add_prompt(self):
        new_prompt, new_completion = "This is a new prompt.", "This is a new completion."
        df = self.get_prompt_data_frame()
        prompt = df.add_prompt(new_prompt, new_completion)
        self.assert_prompt(prompt, new_prompt, new_completion)

        df_empty = PromptDataFrame()
        prompt_empty = df_empty.add_prompt(new_prompt, new_completion)
        self.assert_prompt(prompt_empty, new_prompt, new_completion)

    def assert_prompt(self, prompt_dict: EnumDict, prompt, completion):
        self.assertEqual(prompt_dict[PromptKeys.PROMPT], prompt)
        self.assertEqual(prompt_dict[PromptKeys.COMPLETION], completion)

    def get_prompt_data_frame(self):
        return PromptDataFrame({PromptKeys.PROMPT: ["This is a prompt."], PromptKeys.COMPLETION: ["This is a completion."]})
