import os
from collections import Callable
from typing import Dict, List

import mock

from tgen.data.dataframes.prompt_dataframe import PromptDataFrame
from tgen.data.prompts.creation_prompt_generator import CreationPromptGenerator
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_OUTPUT_DIR
from tgen.testres.testprojects.prompt_test_project import PromptTestProject
from tgen.util.json_util import JsonUtil


class TestResponse:
    id = "id_from_res"


class TestPromptDataset(BaseTest):
    DATASET_FAIL_MSG = "Dataset with param {} failed."

    @mock.patch("openai.File.create")
    def test_get_data_file_id(self, openai_file_create_mock: mock.MagicMock):
        openai_file_create_mock.return_value = TestResponse()
        outputs = self.all_datasets_test(
            lambda dataset: dataset.get_project_file_id(
                prompt_generator=CreationPromptGenerator() if dataset._has_trace_data else None),
        )
        dataset = self.get_dataset_with_prompt_df()
        dataset.data_export_path = TEST_OUTPUT_DIR
        outputs["with_output_path"] = dataset.get_project_file_id(CreationPromptGenerator())
        for type_, file_id in outputs.items():
            fail_msg = self.DATASET_FAIL_MSG.format(type_)
            if type_ == "id":
                self.assertEqual("id", file_id, msg=fail_msg)
            else:
                self.assertEqual("id_from_res", file_id, msg=fail_msg)
        for file in os.listdir(os.getcwd()):
            if file.endswith(".jsonl"):
                self.fail("jsonl file was not deleted like expected")

    def test_export_and_get_dataframe(self):
        outputs = self.all_datasets_test(
            lambda dataset: dataset.export_prompt_dataset(dataset.get_prompts_dataframe(CreationPromptGenerator()),
                                                          TEST_OUTPUT_DIR),
            ["id"]
        )
        dataset = self.get_dataset_with_prompt_df()
        outputs["with_filename"] = dataset.export_prompt_dataset(dataset.get_prompts_dataframe(CreationPromptGenerator()),
                                                                 os.path.join(TEST_OUTPUT_DIR, "file.jsonl"))
        outputs["no_output_path"] = dataset.export_prompt_dataset(dataset.get_prompts_dataframe(CreationPromptGenerator()))
        for type_, output in outputs.items():
            fail_msg = self.DATASET_FAIL_MSG.format(type_)
            export_path, should_delete = output
            prompt_df = PromptDataFrame(JsonUtil.read_jsonl_file(export_path))
            if type_ == "artifact":
                PromptTestProject.verify_prompts_artifacts_project(self, prompt_df, msg=fail_msg)
            else:
                PromptTestProject.verify_prompts_safa_project(self, prompt_df, msg=fail_msg)
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
