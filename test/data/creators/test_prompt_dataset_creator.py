from typing import Dict, List
from unittest import skip

from tgen.constants.open_ai_constants import OPEN_AI_MODEL_DEFAULT
from tgen.core.args.open_ai_args import OpenAIArgs
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.prompts.artifact_prompt import ArtifactPrompt
from tgen.data.prompts.binary_choice_question_prompt import BinaryChoiceQuestionPrompt
from tgen.data.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.data.prompts.prompt_builder import PromptBuilder
from tgen.data.prompts.question_prompt import QuestionPrompt
from tgen.data.summarizer.summarizer import Summarizer
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.test_assertions import TestAssertions
from tgen.testres.testprojects.artifact_test_project import ArtifactTestProject
from tgen.testres.testprojects.mocking.mock_ai_decorator import mock_openai
from tgen.testres.testprojects.mocking.test_open_ai_responses import SUMMARY_FORMAT
from tgen.testres.testprojects.mocking.test_response_manager import TestAIManager
from tgen.testres.testprojects.prompt_test_project import PromptTestProject


class TestPromptDatasetCreator(BaseTest):

    def test_project_reader_artifact(self):
        artifact_project_reader = PromptTestProject.get_artifact_project_reader()
        dataset_creator = self.get_prompt_dataset_creator(project_reader=artifact_project_reader)
        prompt_dataset = dataset_creator.create()
        prompt = QuestionPrompt("Tell me about this artifact:")
        artifact_prompt = ArtifactPrompt(include_id=False)
        prompt_builder = PromptBuilder([prompt, artifact_prompt])
        prompts_df = prompt_dataset.get_prompt_dataframe(prompt_builder, prompt_args=OpenAIManager.prompt_args, )
        PromptTestProject.verify_prompts_artifacts_project(self, prompts_df)

    @mock_openai
    def test_project_reader_artifact_with_summarizer(self, ai_manager: TestAIManager):
        ai_manager.mock_summarization()
        artifact_project_reader = PromptTestProject.get_artifact_project_reader()
        llm_manager = self.create_llm_manager()
        dataset_creator = self.get_prompt_dataset_creator(project_reader=artifact_project_reader,
                                                          summarizer=Summarizer(llm_manager, code_or_exceeds_limit_only=False))

        self.verify_summarization(dataset_creator=dataset_creator, expected_entries=ArtifactTestProject.get_artifact_entries())

    def test_project_reader_prompt(self):
        prompt_project_reader = PromptTestProject.get_project_reader()
        dataset_creator = self.get_prompt_dataset_creator(project_reader=prompt_project_reader)
        artifact_df, trace_df, _ = PromptTestProject.SAFA_PROJECT.get_project_reader().read_project()
        self.verify_dataset_creator(dataset_creator, trace_df=trace_df, use_targets_only=True, include_prompt_builder=False)

    def test_trace_dataset_creator(self):
        trace_dataset_creator = PromptTestProject.get_trace_dataset_creator()
        dataset_creator = self.get_prompt_dataset_creator(trace_dataset_creator=trace_dataset_creator)
        trace_df = dataset_creator.trace_dataset_creator.create().trace_df
        prompt = BinaryChoiceQuestionPrompt(choices=["yes", "no"], question="Are these two artifacts related?")
        prompt2 = MultiArtifactPrompt(data_type=MultiArtifactPrompt.DataType.TRACES)
        prompt_builder = PromptBuilder(prompts=[prompt, prompt2])
        self.verify_dataset_creator(dataset_creator, prompt_builder=prompt_builder, trace_df=trace_df)

    @mock_openai
    def test_trace_dataset_creator_with_summarizer(self, ai_manager: TestAIManager):
        ai_manager.mock_summarization()

        trace_dataset_creator = PromptTestProject.get_trace_dataset_creator()
        llm_manager = self.create_llm_manager()
        dataset_creator: PromptDatasetCreator = self.get_prompt_dataset_creator(trace_dataset_creator=trace_dataset_creator,
                                                                                summarizer=Summarizer(llm_manager,
                                                                                                      code_or_exceeds_limit_only=False))
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

    def verify_dataset_creator(self, dataset_creator: PromptDatasetCreator, trace_df: TraceDataFrame, use_targets_only: bool = False,
                               prompt_builder: PromptBuilder = None, include_prompt_builder: bool = True):
        if prompt_builder is None and include_prompt_builder:
            prompt1 = QuestionPrompt("Tell me about this artifact:")
            prompt2 = MultiArtifactPrompt(data_type=MultiArtifactPrompt.DataType.TRACES)
            prompt_builder = PromptBuilder([prompt1, prompt2])
        prompt_dataset = dataset_creator.create()
        prompts_df = prompt_dataset.get_prompt_dataframe(prompt_builder, prompt_args=OpenAIManager.prompt_args, )
        if not use_targets_only:
            PromptTestProject.verify_prompts_safa_project_traces_for_classification(self, prompts_df, trace_df)
        else:
            PromptTestProject.verify_prompts_safa_project_traces_for_generation(self, prompts_df, trace_df)

    def verify_summarization(self, dataset_creator: PromptDatasetCreator, expected_entries: List[Dict]):
        """
        Verifies that entries are properly summarized by reader
        :return: None
        """
        prompt_dataset: PromptDataset = dataset_creator.create()
        for row in expected_entries:
            row[ArtifactKeys.CONTENT.value] = SUMMARY_FORMAT.format(row[ArtifactKeys.CONTENT.value])
        artifacts_df = prompt_dataset.artifact_df if prompt_dataset.artifact_df is not None \
            else prompt_dataset.trace_dataset.artifact_df
        TestAssertions.verify_entities_in_df(self, expected_entries, artifacts_df)

    @staticmethod
    def get_prompt_dataset_creator(**params):
        return PromptDatasetCreator(**params)

    @staticmethod
    def create_llm_manager() -> AbstractLLMManager:
        return OpenAIManager(OpenAIArgs(model=OPEN_AI_MODEL_DEFAULT))
