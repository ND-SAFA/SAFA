import os
from typing import List, Dict, Any

from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys, ArtifactDataFrame
from tgen.data.dataframes.prompt_dataframe import PromptDataFrame
from tgen.data.dataframes.trace_dataframe import TraceKeys, TraceDataFrame
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
    def get_safa_artifact_id_to_content() -> Dict[Any, str]:
        """
        Gets all the artifacts from the safa project
        :return: A dictionary mapping artifact ids to their content
        """
        return {artifact[ArtifactKeys.ID.value]: artifact[ArtifactKeys.CONTENT.value]
                for artifact in PromptTestProject.get_safa_artifacts()}

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
        artifacts = PromptTestProject.get_safa_artifact_id_to_content()
        for i, (link_id, link) in enumerate(trace_df.itertuples()):
            prompt = prompt_df.get_row(i)
            source_id, target_id = link[TraceKeys.SOURCE], link[TraceKeys.TARGET]
            source, target = artifacts[source_id], artifacts[target_id]
            test_case.assertIn(target, prompt[PromptKeys.PROMPT], **params)
            test_case.assertIn(source, prompt[PromptKeys.PROMPT], **params)

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
        artifacts = PromptTestProject.get_safa_artifact_id_to_content()
        for i, (id_, row) in enumerate(trace_df.itertuples()):
            prompt = prompt_df.get_row(i)
            test_case.assertIn(artifacts[row[TraceKeys.TARGET]], prompt[PromptKeys.PROMPT], **params)

    @staticmethod
    def verify_prompts_safa_project_artifacts(test_case: BaseTest, prompt_df: PromptDataFrame, artifacts_df: ArtifactDataFrame,
                                              **params):
        """
        Verifies the correct prompts are made from the test SAFA project
        :param test_case: The test calling the method
        :param prompt_df: The prompt dataframe to verify
        :param artifacts_df: The artifacts dataframe used to create the prompts
        :return:
        """
        test_case.assertEqual(len(artifacts_df), len(prompt_df), **params)
        for i, (id_, row) in enumerate(artifacts_df.itertuples()):
            prompt = prompt_df.get_row(i)
            test_case.assertIn(row["content"], prompt[PromptKeys.PROMPT], **params)
