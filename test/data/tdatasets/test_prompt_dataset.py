import os
from typing import Callable, Dict, List

import mock
import pandas as pd

from tgen.common.constants.open_ai_constants import MAX_TOKENS_BUFFER, MAX_TOKENS_DEFAULT
from tgen.core.args.open_ai_args import OpenAIArgs
from tgen.data.chunkers.abstract_chunker import AbstractChunker
from tgen.data.keys.structure_keys import TraceKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.models.tokens.token_limits import ModelTokenLimits
from tgen.prompts.artifact_prompt import ArtifactPrompt
from tgen.prompts.multi_artifact_prompt import MultiArtifactPrompt
from tgen.prompts.prompt_builder import PromptBuilder
from tgen.prompts.question_prompt import QuestionPrompt
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_OUTPUT_DIR
from tgen.testres.testprojects.prompt_test_project import PromptTestProject


class TestResponse:
    id = "id_from_res"


class TestPromptDataset(BaseTest):
    DATASET_FAIL_MSG = "Dataset with param {} failed."
    EXCEEDS_TOKEN_LIMIT_ARTIFACT = "3"

    @staticmethod
    def fake_summarize(content, id_=None):
        return "@*&" + content

    @staticmethod
    def fake_exceeds_token_limit(prompt):
        if TestPromptDataset.EXCEEDS_TOKEN_LIMIT_ARTIFACT in prompt:
            return True
        if "@*&" * 2 in prompt:
            return False
        return True

    def test_as_creator(self):
        datasets = self.get_prompt_datasets()
        artifact_dataset = datasets["artifact"]
        creator = artifact_dataset.as_creator(os.path.join(TEST_OUTPUT_DIR, "dir1"))
        recreated_dataset = creator.create()
        self.assertEqual(set(recreated_dataset.artifact_df.index), set(artifact_dataset.artifact_df.index))
        trace_dataset = datasets["dataset"]
        creator = trace_dataset.as_creator(os.path.join(TEST_OUTPUT_DIR, "dir2"))
        recreated_dataset = creator.create()
        self.assertEqual(set(recreated_dataset.artifact_df.index), set(trace_dataset.artifact_df.index))
        for i, link in trace_dataset.trace_dataset.trace_df.itertuples():
            self.assertIsNotNone(recreated_dataset.trace_dataset.trace_df.get_link(source_id=link[TraceKeys.SOURCE],
                                                                                   target_id=link[TraceKeys.TARGET]))

    @mock.patch.object(ModelTokenLimits, "get_token_limit_for_model")
    @mock.patch.object(AbstractChunker, "exceeds_token_limit")
    def test_get_prompt_entry(self, exceeds_token_limit_mock: mock.MagicMock, token_limit_mock: mock.MagicMock):
        token_limit = 5
        token_limit_mock.return_value = token_limit + MAX_TOKENS_BUFFER + MAX_TOKENS_DEFAULT
        exceeds_token_limit_mock.side_effect = self.fake_exceeds_token_limit
        artifact_prompt_dataset: PromptDataset = self.get_prompt_dataset_from_artifact_df()

        llm_manager = OpenAIManager(OpenAIArgs())
        prompt = QuestionPrompt("Tell me about this artifact:")
        prompt_builder = PromptBuilder([prompt, ArtifactPrompt()])
        prompts_df = artifact_prompt_dataset.get_prompt_dataframe(prompt_builders=prompt_builder,
                                                                  prompt_args=llm_manager.prompt_args)

        self.assertEqual(len(prompts_df), len(artifact_prompt_dataset.artifact_df))

        prompt = QuestionPrompt("Tell me about these artifacts:")
        prompt_builder = PromptBuilder([prompt, MultiArtifactPrompt(data_type=MultiArtifactPrompt.DataType.TRACES)])
        traces_prompt_dataset = self.get_dataset_with_trace_dataset()
        prompts_df = traces_prompt_dataset.get_prompt_dataframe(prompt_builder, prompt_args=llm_manager.prompt_args)
        self.assertEqual(len(prompts_df), len(traces_prompt_dataset.trace_dataset.trace_df))

        prompt = QuestionPrompt("Tell me about these artifacts:")
        prompt_builder = PromptBuilder([prompt, MultiArtifactPrompt()])
        prompts_df = traces_prompt_dataset.get_prompt_dataframe(prompt_builder, prompt_args=llm_manager.prompt_args)
        self.assertEqual(len(prompts_df), 1)

    def test_to_dataframe(self):
        outputs = self.run_dataset_tests(
            lambda dataset: dataset.to_dataframe(),
            expected_exceptions=["id"]
        )
        for type_, output in outputs.items():
            self.assertIsInstance(output, pd.DataFrame)

    @mock.patch("openai.File.create")
    def test_get_data_file_id(self, openai_file_create_mock: mock.MagicMock):
        openai_file_create_mock.return_value = TestResponse()
        llm_manager = OpenAIManager(OpenAIArgs())
        prompt = QuestionPrompt("Tell me about this artifact: {target_content}")
        prompt_builder = PromptBuilder([prompt])
        outputs = self.run_dataset_tests(
            lambda dataset: dataset.get_project_file_id(
                llm_manager,
                prompt_builder=prompt_builder if dataset._has_trace_data else None),
        )
        dataset = self.get_dataset_from_prompt_df()
        dataset.data_export_path = TEST_OUTPUT_DIR
        llm_manager = OpenAIManager(OpenAIArgs())
        outputs["with_output_path"] = dataset.get_project_file_id(llm_manager, prompt_builder)
        for type_, file_id in outputs.items():
            fail_msg = self.DATASET_FAIL_MSG.format(type_)
            if type_ == "id":
                self.assertEqual("id", file_id, msg=fail_msg)
            else:
                self.assertEqual("id_from_res", file_id, msg=fail_msg)

    @staticmethod
    def run_dataset_tests(func_to_test: Callable, expected_exceptions: List[str] = None):
        expected_exceptions = expected_exceptions if expected_exceptions else []
        return_vals = {}
        for type_, dataset in TestPromptDataset.get_prompt_datasets().items():
            try:
                res = func_to_test(dataset)
                return_vals[type_] = res
            except Exception as e:
                if type_ in expected_exceptions:
                    continue
                raise e
        return return_vals

    @staticmethod
    def get_prompt_datasets() -> Dict[str, PromptDataset]:
        datasets = {"artifact": TestPromptDataset.get_prompt_dataset_from_artifact_df(),
                    "prompt": TestPromptDataset.get_dataset_from_prompt_df(),
                    "dataset": TestPromptDataset.get_dataset_with_trace_dataset(),
                    "id": TestPromptDataset.get_dataset_with_project_file_id()}
        return datasets

    @staticmethod
    def get_prompt_dataset_from_artifact_df() -> PromptDataset:
        artifact_project_reader = PromptTestProject.get_artifact_project_reader()
        artifact_df = artifact_project_reader.read_project()
        return PromptDataset(artifact_df=artifact_df)

    @staticmethod
    def get_dataset_from_prompt_df():
        prompt_project_reader = PromptTestProject.get_project_reader()
        prompt_df = prompt_project_reader.read_project()
        return PromptDataset(prompt_df=prompt_df)

    @staticmethod
    def get_dataset_with_trace_dataset():
        trace_dataset = PromptTestProject.get_trace_dataset_creator().create()
        return PromptDataset(trace_dataset=trace_dataset)

    @staticmethod
    def get_dataset_with_project_file_id():
        return PromptDataset(project_file_id="id")
