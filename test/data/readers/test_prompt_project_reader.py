import json
import os

import pandas as pd

from tgen.data.readers.prompt_project_reader import PromptProjectReader
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
        self.verify_project_data_frames()

    def verify_project_data_frames(self) -> None:
        """
        Verifies that entries are found in data frames created by project reader.
        :return: None
        """
        project_reader = self.get_project_reader()
        prompts_df = project_reader.read_project()
        expected_prompts = []
        with open(self.PROJECT_PATH) as file:
            for line in file.readlines():
                expected_prompts.append(json.loads(line))
        TestAssertions.verify_entities_in_df(self, expected_prompts, prompts_df)

    def get_project_reader(self) -> PromptProjectReader:
        """
        Gets the prompt project reader for the project
        :return: The prompt project reader for the project
        """
        return PromptProjectReader(self.PROJECT_PATH)
