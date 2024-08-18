import os
from copy import deepcopy
from typing import Dict, List

from gen_common.data.creators.prompt_dataset_creator import PromptDatasetCreator
from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.llm.open_ai_manager import OpenAIManager
from gen_common.llm.prompts.artifact_prompt import ArtifactPrompt
from gen_common.llm.prompts.binary_choice_question_prompt import BinaryChoiceQuestionPrompt
from gen_common.llm.prompts.multi_artifact_prompt import MultiArtifactPrompt
from gen_common.llm.prompts.prompt_builder import PromptBuilder
from gen_common.llm.prompts.question_prompt import QuestionPrompt
from gen_common.summarize.artifact.artifacts_summarizer import ArtifactsSummarizer
from gen_common.util.dataframe_util import DataFrameUtil
from gen_common_test.base.constants import SUMMARY_FORMAT
from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.tests.base_test import BaseTest
from gen_common_test.paths.base_paths import TEST_OUTPUT_DIR
from gen_common_test.testprojects.artifact_test_project import ArtifactTestProject
from gen_common_test.testprojects.prompt_test_project import PromptTestProject


class TestPromptDatasetCreator(BaseTest):
    class FakeArtifactReader:

        def __init__(self, artifact_df: ArtifactDataFrame):
            self.artifact_df = artifact_df
            self.project_path = os.path.join(TEST_OUTPUT_DIR, "prompt_dataset_creator")

        def get_full_project_path(self):
            return self.project_path

        def read_project(self):
            return self.artifact_df

    @mock_anthropic
    def test_project_reader_artifact_with_summarizer(self, ai_manager: TestAIManager):
        ai_manager.mock_summarization()
        artifact_project_reader = PromptTestProject.get_artifact_project_reader()
        dataset_creator = self.get_prompt_dataset_creator(project_reader=artifact_project_reader,
                                                          summarizer=ArtifactsSummarizer(
                                                              summarize_code_only=False))

        self.verify_summarization(dataset_creator=dataset_creator, expected_entries=ArtifactTestProject.get_artifact_entries())

    @mock_anthropic
    def test_trace_dataset_creator_with_summarizer(self, ai_manager: TestAIManager):
        ai_manager.mock_summarization()

        trace_dataset_creator = PromptTestProject.get_trace_dataset_creator()
        dataset_creator: PromptDatasetCreator = self.get_prompt_dataset_creator(trace_dataset_creator=trace_dataset_creator,
                                                                                summarizer=ArtifactsSummarizer(
                                                                                    summarize_code_only=False))
        artifact_entries = self.get_expected_bodies()
        self.verify_summarization(dataset_creator=dataset_creator, expected_entries=artifact_entries)

    def verify_summarization(self, dataset_creator: PromptDatasetCreator, expected_entries: List[Dict]):
        """
        Verifies that entries are properly summarized by reader
        :return: None
        """
        prompt_dataset: PromptDataset = dataset_creator.create()
        for row in expected_entries:
            row[ArtifactKeys.SUMMARY.value] = SUMMARY_FORMAT.format(row[ArtifactKeys.CONTENT.value])
        artifact_df = prompt_dataset.artifact_df if prompt_dataset.artifact_df is not None \
            else prompt_dataset.trace_dataset.artifact_df
        self.verify_entities_in_df(expected_entries, artifact_df)

    def test_project_reader_artifact(self):
        artifact_project_reader = PromptTestProject.get_artifact_project_reader()
        dataset_creator = self.get_prompt_dataset_creator(project_reader=artifact_project_reader)
        prompt_dataset = dataset_creator.create()
        prompt = QuestionPrompt("Tell me about this artifact:")
        artifact_prompt = ArtifactPrompt(include_id=False)
        prompt_builder = PromptBuilder([prompt, artifact_prompt])
        prompts_df = prompt_dataset.get_prompt_dataframe(prompt_builder, prompt_args=OpenAIManager.prompt_args, )
        PromptTestProject.verify_prompts_artifacts_project(self, prompts_df)

    def test_project_reader_prompt(self):
        prompt_project_reader = PromptTestProject.get_project_reader()
        dataset_creator = self.get_prompt_dataset_creator(project_reader=prompt_project_reader)
        artifact_df, trace_df, _ = PromptTestProject.SAFA_PROJECT.get_project_reader().read_project()
        PromptTestProject.verify_dataset_creator(self, dataset_creator, trace_df=trace_df, use_targets_only=True,
                                                 include_prompt_builder=False)

    def test_trace_dataset_creator(self):
        trace_dataset_creator = PromptTestProject.get_trace_dataset_creator()
        dataset_creator = self.get_prompt_dataset_creator(trace_dataset_creator=trace_dataset_creator)
        trace_df = dataset_creator.trace_dataset_creator.create().trace_df
        prompt = BinaryChoiceQuestionPrompt(choices=["yes", "no"], question="Are these two artifacts related?")
        prompt2 = MultiArtifactPrompt(data_type=MultiArtifactPrompt.DataType.TRACES)
        prompt_builder = PromptBuilder(prompts=[prompt, prompt2])
        PromptTestProject.verify_dataset_creator(self, dataset_creator, prompt_builder=prompt_builder, trace_df=trace_df)

    @staticmethod
    def get_expected_bodies():
        artifact_entries = [{ArtifactKeys.CONTENT.value: a[ArtifactKeys.CONTENT.value]} for a in
                            PromptTestProject.get_safa_artifacts()]
        return artifact_entries

    def test_project_file_id(self):
        dataset_creator = self.get_prompt_dataset_creator(project_file_id="id")
        trace_dataset = dataset_creator.create()
        self.assertEqual(trace_dataset.project_file_id, "id")

    @mock_anthropic
    def test_dataset_creator_with_no_code_summaries(self, anthropic_ai_manager: TestAIManager):
        anthropic_ai_manager.mock_summarization()

        artifacts_ids = ["a1", "code.py", "a2", "code.c"]
        artifact_bodies = ["content" for _ in artifacts_ids]
        artifact_layers = ["NL", "PY", "NL", "C"]
        artifact_reader = self.FakeArtifactReader(artifact_df=ArtifactDataFrame({"id": artifacts_ids, "content": artifact_bodies,
                                                                                 "layer_id": artifact_layers}))
        dataset_creator = self.get_prompt_dataset_creator(project_reader=artifact_reader, ensure_code_is_summarized=True)
        dataset1 = dataset_creator.create()
        number_of_summarization_calls = deepcopy(anthropic_ai_manager.mock_calls)
        dataset2 = dataset_creator.create()  # ensure summaries are reused
        self.assertEqual(number_of_summarization_calls, anthropic_ai_manager.mock_calls)
        for dataset in [dataset1, dataset2]:
            for i, artifact_info in enumerate(dataset.artifact_df.itertuples()):
                id_, artifact = artifact_info
                summary = artifact[ArtifactKeys.SUMMARY]
                if artifact_layers[i] == "NL":
                    self.assertIsNone(DataFrameUtil.get_optional_value(summary))
                else:
                    self.assertIn("summary", summary.lower())

    @staticmethod
    def get_prompt_dataset_creator(ensure_code_is_summarized=False, **params):
        return PromptDatasetCreator(**params, ensure_code_is_summarized=ensure_code_is_summarized)
