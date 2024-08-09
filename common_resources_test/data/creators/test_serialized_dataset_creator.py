import os
from copy import deepcopy
from typing import Dict, List

from common_resources.llm.open_ai_manager import OpenAIManager
from common_resources.llm.prompts.artifact_prompt import ArtifactPrompt
from common_resources.llm.prompts.binary_choice_question_prompt import BinaryChoiceQuestionPrompt
from common_resources.llm.prompts.multi_artifact_prompt import MultiArtifactPrompt
from common_resources.llm.prompts.prompt_builder import PromptBuilder
from common_resources.llm.prompts.question_prompt import QuestionPrompt
from common_resources.data.summarizer.artifacts_summarizer import ArtifactsSummarizer
from common_resources.mocking.mock_anthropic import mock_anthropic
from common_resources.mocking.test_open_ai_responses import SUMMARY_FORMAT
from common_resources.mocking.test_response_manager import TestAIManager

from common_resources.data.creators.prompt_dataset_creator import PromptDatasetCreator
from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.keys.structure_keys import ArtifactKeys
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.tools.util.dataframe_util import DataFrameUtil
from common_resources_test.base_tests.base_test import BaseTest
from common_resources_test.paths.base_paths import TEST_OUTPUT_DIR
from common_resources_test.testprojects.artifact_test_project import ArtifactTestProject
from common_resources_test.testprojects.prompt_test_project import PromptTestProject


class TestSerializedDatasetCreator(BaseTest):

    def test_trace_dataset_creator(self):
        trace_dataset_creator = PromptTestProject.get_trace_dataset_creator()
        dataset_creator = self.get_prompt_dataset_creator(trace_dataset_creator=trace_dataset_creator)
        trace_df = dataset_creator.trace_dataset_creator.create().trace_df
        prompt = BinaryChoiceQuestionPrompt(choices=["yes", "no"], question="Are these two artifacts related?")
        prompt2 = MultiArtifactPrompt(data_type=MultiArtifactPrompt.DataType.TRACES)
        prompt_builder = PromptBuilder(prompts=[prompt, prompt2])
        PromptTestProject.verify_dataset_creator(self, dataset_creator, prompt_builder=prompt_builder, trace_df=trace_df)


    @staticmethod
    def get_prompt_dataset_creator(ensure_code_is_summarized=False, **params):
        return PromptDatasetCreator(**params, ensure_code_is_summarized=ensure_code_is_summarized)
