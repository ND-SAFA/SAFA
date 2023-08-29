import os
from typing import Any, Dict, List

from tgen.common.artifact import Artifact
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.prompt_dataframe import PromptDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.readers.artifact_project_reader import ArtifactProjectReader
from tgen.data.readers.prompt_project_reader import PromptProjectReader
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_DATA_DIR
from tgen.testres.testprojects.artifact_test_project import ArtifactTestProject
from tgen.testres.testprojects.safa_test_project import SafaTestProject


class PromptTestProject:
    DATA_PATH = os.path.join(TEST_DATA_DIR, "prompt", "safa_proj.jsonl")

    SAFA_PROJECT = SafaTestProject()

    @staticmethod
    def get_artifact_project_reader() -> ArtifactProjectReader:
        """
        Gets the project reader for artifacts project
        :return: The project reader
        """
        return ArtifactTestProject().get_project_reader()

    @staticmethod
    def get_project_reader() -> PromptProjectReader:
        """
        Gets the project reader for the prompt project
        :return: The project reader
        """
        return PromptProjectReader(project_path=PromptTestProject.DATA_PATH)

    @staticmethod
    def get_trace_dataset_creator() -> TraceDatasetCreator:
        """
        Gets the trace dataset to use for the prompts
        :return: The trace dataset to use for the prompts
        """
        project_reader = SafaTestProject().get_project_reader()
        return TraceDatasetCreator(project_reader)

    @staticmethod
    def get_safa_artifacts() -> List[Artifact]:
        """
        Gets all the artifacts from the safa project
        :return: A list of all artifacts as dicts
        """
        artifacts = PromptTestProject.SAFA_PROJECT.get_source_artifacts() + PromptTestProject.SAFA_PROJECT.get_target_artifacts()
        return artifacts

    @staticmethod
    def get_artifact_map() -> Dict[Any, str]:
        """
        Gets all the artifacts from the safa project
        :return: A dictionary mapping artifact ids to their content
        """
        artifacts = PromptTestProject.get_safa_artifacts()
        return {a[ArtifactKeys.ID.value]: a[ArtifactKeys.CONTENT.value] for a in artifacts}

    @staticmethod
    def verify_prompts_artifacts_project(test_case: BaseTest, prompts_df: PromptDataFrame, **params):
        """
        Verifies the correct prompts are made from the test Artifacts project
        :param test_case: The test calling the method
        :param prompts_df: The prompt dataframe to verify
        :return:
        """
        artifacts = PromptTestProject.get_safa_artifacts()
        test_case.assertEqual(len(prompts_df), len(artifacts), **params)
        for artifact in artifacts:
            content = artifact[ArtifactKeys.CONTENT.value]
            found = False
            for i, row in prompts_df.itertuples():
                prompt = row[PromptKeys.PROMPT]
                if content in prompt:
                    found = True
                    break
            test_case.assertTrue(found, msg=f"Could not find artifact: {artifact}")

    @staticmethod
    def verify_prompts_safa_project_traces_for_classification(test_case: BaseTest, prompt_df: PromptDataFrame,
                                                              trace_df: TraceDataFrame, **params):
        """
        Verifies the correct prompts are made from the test SAFA project
        :param test_case: The test calling the method
        :param prompt_df: The prompt dataframe to verify
        :param trace_df: The trace dataframe used to create the prompts
        :return:
        """
        test_case.assertEqual(len(trace_df), len(prompt_df), **params)
        artifacts = PromptTestProject.get_artifact_map()
        for i, (link_id, link) in enumerate(trace_df.itertuples()):
            source_id, target_id = link[TraceKeys.SOURCE], link[TraceKeys.TARGET]
            source_body, target_body = artifacts[source_id], artifacts[target_id]
            found = False
            for j, prompt_row in prompt_df.iterrows():
                prompt = prompt_row[PromptKeys.PROMPT.value]
                if target_body in prompt and source_body in prompt:
                    found = True
                    break
            test_case.assertTrue(found, msg=f"Unable to find prompt with {source_id} and {target_id}.")

    @staticmethod
    def verify_prompts_safa_project_traces_for_generation(test_case: BaseTest, prompt_df: PromptDataFrame, trace_df: TraceDataFrame,
                                                          **params):
        """
        Verifies the correct prompts are made from the test SAFA project
        :param test_case: The test calling the method
        :param prompt_df: The prompt dataframe to verify
        :param trace_df: The trace dataframe used to create the prompts
        :return:
        """
        test_case.assertEqual(len(trace_df), len(prompt_df), **params)
        artifact_map = PromptTestProject.get_artifact_map()
        for i, (_, row) in enumerate(trace_df.itertuples()):
            prompt_row = prompt_df.get_row(i)
            parent_id = row[TraceKeys.TARGET]
            artifact_content = artifact_map[parent_id]
            prompt = prompt_row[PromptKeys.PROMPT]
            test_case.assertIn(artifact_content, prompt, **params)

    @staticmethod
    def verify_prompts_safa_project_artifacts(test_case: BaseTest, prompt_df: PromptDataFrame, artifact_df: ArtifactDataFrame,
                                              **params):
        """
        Verifies the correct prompts are made from the test SAFA project
        :param test_case: The test calling the method
        :param prompt_df: The prompt dataframe to verify
        :param artifact_df: The artifacts dataframe used to create the prompts
        :return:
        """
        test_case.assertEqual(len(artifact_df), len(prompt_df), **params)
        for i, (id_, row) in enumerate(artifact_df.itertuples()):
            prompt = prompt_df.get_row(i)
            test_case.assertIn(row["content"], prompt[PromptKeys.PROMPT], **params)
