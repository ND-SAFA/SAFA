import os
from copy import deepcopy
from typing import Dict, List
from unittest import mock
from unittest.mock import MagicMock

from tgen.common.util.dataframe_util import DataFrameUtil
from tgen.common.util.enum_util import EnumDict
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.binary_choice_question_prompt import BinaryChoiceQuestionPrompt
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.question_prompt import QuestionPrompt
from tgen.summarizer.artifact.artifacts_summarizer import ArtifactsSummarizer
from tgen.summarizer.project.project_summarizer import ProjectSummarizer
from tgen.summarizer.summary import Summary
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_open_ai_responses import SUMMARY_FORMAT
from tgen.testres.mocking.test_response_manager import TestAIManager
from tgen.testres.paths.paths import TEST_OUTPUT_DIR
from tgen.testres.test_assertions import TestAssertions
from tgen.testres.testprojects.artifact_test_project import ArtifactTestProject
from tgen.testres.testprojects.prompt_test_project import PromptTestProject


class TestPromptDatasetCreator(BaseTest):
    class FakeArtifactReader:

        def __init__(self, artifact_df: ArtifactDataFrame):
            self.artifact_df = artifact_df
            self.project_path = os.path.join(TEST_OUTPUT_DIR, "prompt_dataset_creator")

        def get_full_project_path(self):
            return self.project_path

        def read_project(self):
            return self.artifact_df

    def test_project_reader_artifact(self):
        artifact_project_reader = PromptTestProject.get_artifact_project_reader()
        dataset_creator = self.get_prompt_dataset_creator(project_reader=artifact_project_reader)
        prompt_dataset = dataset_creator.create()
        prompt = QuestionPrompt("Tell me about this artifact:")
        artifact_prompt = ArtifactPrompt(include_id=False)
        prompt_builder = PromptBuilder([prompt, artifact_prompt])
        prompts_df = prompt_dataset.get_prompt_dataframe(prompt_builder, prompt_args=OpenAIManager.prompt_args, )
        PromptTestProject.verify_prompts_artifacts_project(self, prompts_df)

    @mock_anthropic
    def test_project_reader_artifact_with_summarizer(self, ai_manager: TestAIManager):
        ai_manager.mock_summarization()
        artifact_project_reader = PromptTestProject.get_artifact_project_reader()
        dataset_creator = self.get_prompt_dataset_creator(project_reader=artifact_project_reader,
                                                          summarizer=ArtifactsSummarizer(
                                                              summarize_code_only=False))

        self.verify_summarization(dataset_creator=dataset_creator, expected_entries=ArtifactTestProject.get_artifact_entries())

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

    @mock_anthropic
    def test_trace_dataset_creator_with_summarizer(self, ai_manager: TestAIManager):
        ai_manager.mock_summarization()

        trace_dataset_creator = PromptTestProject.get_trace_dataset_creator()
        dataset_creator: PromptDatasetCreator = self.get_prompt_dataset_creator(trace_dataset_creator=trace_dataset_creator,
                                                                                summarizer=ArtifactsSummarizer(
                                                                                    summarize_code_only=False))
        artifact_entries = self.get_expected_bodies()
        self.verify_summarization(dataset_creator=dataset_creator, expected_entries=artifact_entries)

    @staticmethod
    def get_expected_bodies():
        artifact_entries = [{ArtifactKeys.CONTENT.value: a[ArtifactKeys.CONTENT.value]} for a in
                            PromptTestProject.get_safa_artifacts()]
        return artifact_entries

    def test_project_file_id(self):
        dataset_creator = self.get_prompt_dataset_creator(project_file_id="id")
        trace_dataset = dataset_creator.create()
        self.assertEqual(trace_dataset.project_file_id, "id")

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
        TestAssertions.verify_entities_in_df(self, expected_entries, artifact_df)

    @mock.patch.object(ProjectSummarizer, "summarize")
    @mock_anthropic
    def test_dataset_creator_with_no_code_summaries(self, anthropic_ai_manager: TestAIManager, project_summarizer_mock: MagicMock):
        # contains no summaries so all should be summarized
        project_summary = Summary(overview=EnumDict({"chunks": ["summary of project"],
                                                     "title": "overview"}))
        project_summarizer_mock.return_value = project_summary
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
