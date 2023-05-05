import os
from collections import Callable
from typing import Dict, List

import mock
import pandas as pd

from tgen.constants.open_ai_constants import MAX_TOKENS_BUFFER, MAX_TOKENS_DEFAULT
from tgen.data.chunkers.abstract_chunker import AbstractChunker
from tgen.data.dataframes.prompt_dataframe import PromptDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.generation_prompt_creator import GenerationPromptCreator
from tgen.data.summarizer.summarizer import Summarizer
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.models.token_limits import ModelTokenLimits
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_OUTPUT_DIR
from tgen.testres.testprojects.prompt_test_project import PromptTestProject
from tgen.train.args.open_ai_args import OpenAIArgs
from tgen.util.dataframe_util import DataFrameUtil
from tgen.util.json_util import JsonUtil


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

    @mock.patch.object(ModelTokenLimits, "get_token_limit_for_model")
    @mock.patch.object(Summarizer, "summarize")
    @mock.patch.object(AbstractChunker, "exceeds_token_limit")
    def test_get_prompt_entry(self, exceeds_token_limit_mock: mock.MagicMock,
                              summarize_mock: mock.MagicMock, token_limit_mock: mock.MagicMock):
        token_limit = 5
        token_limit_mock.return_value = token_limit + MAX_TOKENS_BUFFER + MAX_TOKENS_DEFAULT
        exceeds_token_limit_mock.side_effect = self.fake_exceeds_token_limit
        summarize_mock.side_effect = self.fake_summarize
        artifact_prompt_dataset = self.get_dataset_with_artifact_df()
        llm_manager = OpenAIManager(OpenAIArgs())
        prompts_df = artifact_prompt_dataset._generate_prompts_dataframe_from_artifacts(GenerationPromptCreator(),
                                                                                        Summarizer(llm_manager))
        for i, artifact_id in enumerate(artifact_prompt_dataset.artifact_df.index):
            if TestPromptDataset.EXCEEDS_TOKEN_LIMIT_ARTIFACT in artifact_id:
                self.assertEqual(len(prompts_df.get_row(i)[PromptKeys.PROMPT].split()), token_limit)
        self.assertEqual(len(prompts_df), len(artifact_prompt_dataset.artifact_df))

        traces_prompt_dataset = self.get_dataset_with_trace_dataset()
        prompts_df = traces_prompt_dataset._generate_prompts_dataframe_from_traces(GenerationPromptCreator(), Summarizer(llm_manager))
        self.assertEqual(len(prompts_df), len(traces_prompt_dataset.trace_dataset.trace_df))

    def test_to_dataframe(self):
        outputs = self.all_datasets_test(
            lambda dataset: dataset.to_dataframe(),
            expected_exceptions=["id"]
        )
        for type_, output in outputs.items():
            self.assertIsInstance(output, pd.DataFrame)

    @mock.patch("openai.File.create")
    def test_get_data_file_id(self, openai_file_create_mock: mock.MagicMock):
        openai_file_create_mock.return_value = TestResponse()
        llm_manager = OpenAIManager(OpenAIArgs())
        outputs = self.all_datasets_test(
            lambda dataset: dataset.get_project_file_id(
                llm_manager,
                prompt_creator=GenerationPromptCreator() if dataset._has_trace_data else None),
        )
        dataset = self.get_dataset_with_prompt_df()
        dataset.data_export_path = TEST_OUTPUT_DIR
        llm_manager = OpenAIManager(OpenAIArgs())
        outputs["with_output_path"] = dataset.get_project_file_id(llm_manager, GenerationPromptCreator())
        for type_, file_id in outputs.items():
            fail_msg = self.DATASET_FAIL_MSG.format(type_)
            if type_ == "id":
                self.assertEqual("id", file_id, msg=fail_msg)
            else:
                self.assertEqual("id_from_res", file_id, msg=fail_msg)

    def test_export_and_get_dataframe(self):
        prompt_creator = GenerationPromptCreator()
        outputs = self.all_datasets_test(
            lambda dataset: dataset.export_prompt_dataframe(dataset.get_prompts_dataframe(prompt_creator),
                                                            TEST_OUTPUT_DIR),
            ["id"]
        )
        dataset = self.get_dataset_with_prompt_df()
        outputs["with_filename"] = dataset.export_prompt_dataframe(dataset.get_prompts_dataframe(GenerationPromptCreator()),
                                                                   os.path.join(TEST_OUTPUT_DIR, "file.jsonl"))
        outputs["no_output_path"] = dataset.export_prompt_dataframe(dataset.get_prompts_dataframe(GenerationPromptCreator()))
        expected_trace_dataset = PromptTestProject.get_trace_dataset_creator().create()
        for type_, output in outputs.items():
            fail_msg = self.DATASET_FAIL_MSG.format(type_)
            export_path, should_delete = output
            prompt_df = PromptDataFrame(JsonUtil.read_jsonl_file(export_path))
            if type_ == "artifact":
                PromptTestProject.verify_prompts_artifacts_project(self, prompt_df, msg=fail_msg)
            elif type_ == "dataset":
                PromptTestProject.verify_prompts_safa_project_artifacts(self, prompt_df,
                                                                        artifacts_df=expected_trace_dataset.artifact_df,
                                                                        msg=fail_msg, )
            else:
                pos_links_df = TraceDataFrame(DataFrameUtil.filter_df_by_row(expected_trace_dataset.trace_df,
                                                                             lambda row: row[TraceKeys.LABEL.value] == 1))
                PromptTestProject.verify_prompts_safa_project_traces_for_generation(self, prompt_df, trace_df=pos_links_df,
                                                                                    msg=fail_msg)
            if type_ == "no_output_path":
                self.assertTrue(should_delete, msg=fail_msg)
                os.remove(export_path)
            else:
                self.assertFalse(should_delete, msg=fail_msg)

    @staticmethod
    def all_datasets_test(func_to_test: Callable, expected_exceptions: List[str] = None):
        expected_exceptions = expected_exceptions if expected_exceptions else []
        return_vals = {}
        for type_, dataset in TestPromptDataset.get_all_datasets().items():
            try:
                return_vals[type_] = func_to_test(dataset)
            except Exception as e:
                if type_ in expected_exceptions:
                    continue
                raise e
        return return_vals

    @staticmethod
    def get_all_datasets() -> Dict[str, PromptDataset]:
        datasets = {"artifact": TestPromptDataset.get_dataset_with_artifact_df(),
                    "prompt": TestPromptDataset.get_dataset_with_prompt_df(),
                    "dataset": TestPromptDataset.get_dataset_with_trace_dataset(),
                    "id": TestPromptDataset.get_dataset_with_project_file_id()}
        return datasets

    @staticmethod
    def get_dataset_with_artifact_df():
        artifact_project_reader = PromptTestProject.get_artifact_project_reader()
        artifacts_df = artifact_project_reader.read_project()
        return PromptDataset(artifact_df=artifacts_df)

    @staticmethod
    def get_dataset_with_prompt_df():
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
