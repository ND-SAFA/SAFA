import json
import os

from common_resources.data.keys.prompt_keys import PromptKeys
from common_resources.data.readers.prompt_project_reader import PromptProjectReader
from tgen.summarizer.artifact.artifacts_summarizer import ArtifactsSummarizer
from tgen.testres.base_tests.base_test import BaseTest
from common_resources.mocking.mock_anthropic import mock_anthropic
from common_resources.mocking.test_open_ai_responses import SUMMARY_FORMAT
from common_resources.mocking.test_response_manager import TestAIManager
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

    @mock_anthropic
    def test_summarization(self, ai_manager: TestAIManager):
        """
        Tests that project artifacts can be summarized
        """
        ai_manager.mock_summarization()
        project_reader = self.get_project_reader()
        project_reader.set_summarizer(ArtifactsSummarizer(summarize_code_only=False))
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
