import json
import os
from unittest import mock

import pandas as pd

from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.readers.prompt_project_reader import PromptProjectReader
from tgen.data.summarizer.summarizer import Summarizer
from tgen.testres.base_tests.abstract_project_reader_test import SUMMARY_FORMAT, fake_open_ai_completion
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_DATA_DIR
from tgen.testres.test_assertions import TestAssertions


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

    @mock.patch("openai.Completion.create", )
    def test_summarization(self, mock_completion: mock.MagicMock):
        """
        Tests that project artifacts can be summarized
        """
        mock_completion.side_effect = fake_open_ai_completion
        project_reader = self.get_project_reader()
        project_reader.set_summarizer(Summarizer())
        prompts_df = project_reader.read_project()
        expected_prompts = []
        with open(self.PROJECT_PATH) as file:
            for line in file.readlines():
                prompt_dict = json.loads(line)
                prompt_dict[PromptKeys.PROMPT.value] = SUMMARY_FORMAT.format(prompt_dict[PromptKeys.PROMPT.value])
                expected_prompts.append(prompt_dict)
        for i, row in prompts_df.iterrows():
            row[PromptKeys.PROMPT.value] = row[PromptKeys.PROMPT.value] + "\n\n"
        TestAssertions.verify_entities_in_df(self, expected_prompts, prompts_df)

    def get_project_reader(self) -> PromptProjectReader:
        """
        Gets the prompt project reader for the project
        :return: The prompt project reader for the project
        """
        return PromptProjectReader(self.PROJECT_PATH)
