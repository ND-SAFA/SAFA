import os
from typing import Any, Dict, List, Union

from gen_common.data.objects.artifact import Artifact
from gen_common.data.creators.prompt_dataset_creator import PromptDatasetCreator
from gen_common.data.creators.trace_dataset_creator import TraceDatasetCreator
from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.dataframes.prompt_dataframe import PromptDataFrame
from gen_common.data.dataframes.trace_dataframe import TraceDataFrame
from gen_common.data.keys.structure_keys import TraceKeys, ArtifactKeys
from gen_common.data.keys.prompt_keys import PromptKeys
from gen_common.data.readers.artifact_project_reader import ArtifactProjectReader
from gen_common.data.readers.prompt_project_reader import PromptProjectReader
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.llm.open_ai_manager import OpenAIManager
from gen_common.llm.prompts.multi_artifact_prompt import MultiArtifactPrompt
from gen_common.llm.prompts.prompt_builder import PromptBuilder
from gen_common.llm.prompts.question_prompt import QuestionPrompt
from gen_common_test.base_tests.base_test import BaseTest
from gen_common_test.paths.base_paths import TEST_DATA_DIR
from gen_common_test.testprojects.artifact_test_project import ArtifactTestProject
from gen_common_test.testprojects.safa_test_project import SafaTestProject


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
    def verify_dataset(test_case: BaseTest, dataset: Union[PromptDataset, PromptDatasetCreator], **params):
        """
        Verifies the correct prompts are made from the test Artifacts project
        :param test_case: The test calling the method
        :param dataset: The prompt dataset to verify
        :return:
        """
        if isinstance(dataset, PromptDatasetCreator):
            artifact_df, trace_df, _ = PromptTestProject.SAFA_PROJECT.get_project_reader().read_project()
            return PromptTestProject.verify_dataset_creator(test_case, dataset, trace_df=trace_df, use_targets_only=True,
                                                            include_prompt_builder=False)
        artifacts = PromptTestProject.get_safa_artifacts()
        test_case.assertEqual(len(dataset.artifact_df), len(artifacts), **params)
        for artifact in artifacts:
            test_case.assertIn(artifact[ArtifactKeys.ID.value], dataset.artifact_df)
        if dataset.trace_dataset:
            traces = PromptTestProject.get_trace_dataset_creator().create()
            for id_, trace in traces.trace_df.itertuples():
                test_case.assertIn(id_, dataset.trace_dataset.trace_df)

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

    @staticmethod
    def verify_dataset_creator(test_case, dataset_creator: PromptDatasetCreator, trace_df: TraceDataFrame,
                               use_targets_only: bool = False,
                               prompt_builder: PromptBuilder = None, include_prompt_builder: bool = True):
        if prompt_builder is None and include_prompt_builder:
            prompt1 = QuestionPrompt("Tell me about this artifact:")
            prompt2 = MultiArtifactPrompt(data_type=MultiArtifactPrompt.DataType.TRACES)
            prompt_builder = PromptBuilder([prompt1, prompt2])
        prompt_dataset = dataset_creator.create()
        prompts_df = prompt_dataset.get_prompt_dataframe(prompt_builder, prompt_args=OpenAIManager.prompt_args, )
        if not use_targets_only:
            PromptTestProject.verify_prompts_safa_project_traces_for_classification(test_case, prompts_df, trace_df)
        else:
            PromptTestProject.verify_prompts_safa_project_traces_for_generation(test_case, prompts_df, trace_df)
