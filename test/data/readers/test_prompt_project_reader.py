import json
import os
from unittest import mock

from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.readers.prompt_project_reader import PromptProjectReader
from tgen.data.summarizer.summarizer import Summarizer
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_DATA_DIR
from tgen.testres.test_assertions import TestAssertions
from tgen.testres.test_open_ai_responses import SUMMARY_FORMAT, fake_open_ai_completion
from tgen.train.args.open_ai_args import OpenAIArgs


class TestPromptProjectReader(BaseTest):
    """
    Tests that csv project is correctly parsed.
    """
    PROJECT_PATH = os.path.join(TEST_DATA_DIR, "prompt", "lhp.jsonl")

    def test_read_project(self):
        """
        Tests that the csv project can be read and translated to data frames.
        """
        project_reader = self.get_project_reader()
        prompts_df = project_reader.read_project()
        expected_prompts = []
        with open(self.PROJECT_PATH) as file:
            for line in file.readlines():
                expected_prompts.append(json.loads(line))
        TestAssertions.verify_entities_in_df(self, expected_prompts, prompts_df)

    @mock.patch("openai.ChatCompletion.create", )
    def test_summarization(self, mock_completion: mock.MagicMock):
        """
        Tests that project artifacts can be summarized
        """
        mock_completion.side_effect = fake_open_ai_completion
        project_reader = self.get_project_reader()
        llm_manager = OpenAIManager(OpenAIArgs())
        project_reader.set_summarizer(Summarizer(llm_manager, code_or_exceeds_limit_only=False))
        prompts_df = project_reader.read_project()
        expected_prompts = []
        with open(self.PROJECT_PATH) as file:
            for line in file.readlines():
                prompt_dict = json.loads(line)
                prompt_dict[PromptKeys.PROMPT.value] = SUMMARY_FORMAT.format(prompt_dict[PromptKeys.PROMPT.value]) \
                    .replace(os.linesep, "")
                expected_prompts.append(prompt_dict)
        prompts_df[PromptKeys.PROMPT] = [row[PromptKeys.PROMPT].replace(os.linesep, "") for i, row in prompts_df.itertuples()]
        TestAssertions.verify_entities_in_df(self, expected_prompts, prompts_df)

    def get_project_reader(self) -> PromptProjectReader:
        """
        Gets the prompt project reader for the project
        :return: The prompt project reader for the project
        """
        return PromptProjectReader(self.PROJECT_PATH)
