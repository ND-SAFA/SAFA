import os
from typing import List, Dict

from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.prompt_dataframe import PromptDataFrame
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.creation_prompt_generator import CreationPromptGenerator
from tgen.data.readers.artifact_project_reader import ArtifactProjectReader
from tgen.data.readers.prompt_project_reader import PromptProjectReader
from tgen.data.tdatasets.prompt_dataset import PromptDataset
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
    def get_safa_artifacts() -> List[Dict]:
        """
        Gets all the artifacts from the safa project
        :return: A list of all artifacts as dicts
        """
        source_layers = PromptTestProject.SAFA_PROJECT.get_source_entries()
        target_layers = PromptTestProject.SAFA_PROJECT.get_target_entries()
        artifacts = []
        for i, layer in enumerate(source_layers):
            artifacts.extend(layer)
            artifacts.extend((target_layers[i]))
        return artifacts

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
        for i, row in prompts_df.itertuples():
            tokens = artifacts[i][ArtifactKeys.CONTENT.value]
            test_case.assertIn(tokens, row[PromptKeys.PROMPT], **params)

    @staticmethod
    def verify_prompts_safa_project(test_case: BaseTest, prompt_df: PromptDataFrame, **params):
        """
        Verifies the correct prompts are made from the test SAFA project
        :param test_case: The test calling the method
        :param prompt_df: The prompt dataframe to verify
        :return:
        """
        entries = PromptTestProject.SAFA_PROJECT.get_trace_entries()
        test_case.assertEqual(len(entries), len(prompt_df), **params)
        artifacts = {artifact[ArtifactKeys.ID.value]: artifact[ArtifactKeys.CONTENT.value]
                     for artifact in PromptTestProject.get_safa_artifacts()}
        for i, row in prompt_df.itertuples():
            entry = entries[i]
            source_id, target_id = entry[TraceKeys.SOURCE.value], entry[TraceKeys.TARGET.value]
            source, target = artifacts[source_id], artifacts[target_id]
            test_case.assertIn(target, row[PromptKeys.PROMPT], **params)
            test_case.assertIn(source, row[PromptKeys.COMPLETION], **params)
