from unittest import mock

from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.prompts.creation_prompt_generator import CreationPromptGenerator
from tgen.data.summarizer.summarizer import Summarizer
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.testres.base_tests.base_test import BaseTest, SUMMARY_FORMAT, fake_open_ai_completion
from tgen.testres.test_assertions import TestAssertions
from tgen.testres.testprojects.artifact_test_project import ArtifactTestProject
from tgen.testres.testprojects.prompt_test_project import PromptTestProject
from tgen.testres.testprojects.safa_test_project import SafaTestProject


class TestPromptDatasetCreator(BaseTest):

    def test_project_reader_artifact(self):
        artifact_project_reader = PromptTestProject.get_artifact_project_reader()
        dataset_creator = self.get_prompt_dataset_creator(project_reader=artifact_project_reader)
        prompt_dataset = dataset_creator.create()
        prompts_df = prompt_dataset.get_prompts_dataframe(CreationPromptGenerator())
        PromptTestProject.verify_prompts_artifacts_project(self, prompts_df)

    def test_project_reader_artifact_with_summarizer(self):
        artifact_project_reader = PromptTestProject.get_artifact_project_reader()
        dataset_creator = self.get_prompt_dataset_creator(project_reader=artifact_project_reader,
                                                          summarizer=Summarizer())

        self.verify_summarization(dataset_creator=dataset_creator, artifacts_entries=ArtifactTestProject.get_artifact_entries())

    def test_project_reader_prompt(self):
        prompt_project_reader = PromptTestProject.get_project_reader()
        dataset_creator = self.get_prompt_dataset_creator(project_reader=prompt_project_reader)
        self.verify_dataset_creator(dataset_creator)

    def test_trace_dataset_creator(self):
        trace_dataset_creator = PromptTestProject.get_trace_dataset_creator()
        dataset_creator = self.get_prompt_dataset_creator(trace_dataset_creator=trace_dataset_creator)
        self.verify_dataset_creator(dataset_creator)

    def test_trace_dataset_creator_with_summarizer(self):
        trace_dataset_creator = PromptTestProject.get_trace_dataset_creator()
        dataset_creator = self.get_prompt_dataset_creator(trace_dataset_creator=trace_dataset_creator,
                                                          summarizer=Summarizer())
        all_artifacts = {artifact[ArtifactKeys.ID.value]: artifact[ArtifactKeys.CONTENT.value]
                         for artifact in PromptTestProject.get_safa_artifacts()}
        artifact_entries = []
        ids = set()
        for trace in PromptTestProject.SAFA_PROJECT.get_trace_entries():
            if trace[TraceKeys.SOURCE.value] not in ids:
                artifact_entries.append({ArtifactKeys.CONTENT.value: all_artifacts[trace[TraceKeys.SOURCE.value]]})
                ids.add(trace[TraceKeys.SOURCE.value])
            if trace[TraceKeys.TARGET.value] not in ids:
                artifact_entries.append({ArtifactKeys.CONTENT.value: all_artifacts[trace[TraceKeys.TARGET.value]]})
                ids.add(trace[TraceKeys.TARGET.value])
        self.verify_summarization(dataset_creator=dataset_creator, artifacts_entries=artifact_entries)

    def test_project_file_id(self):
        dataset_creator = self.get_prompt_dataset_creator(project_file_id="id")
        trace_dataset = dataset_creator.create()
        self.assertEqual(trace_dataset.project_file_id, "id")

    def verify_dataset_creator(self, dataset_creator: PromptDatasetCreator):
        prompt_dataset = dataset_creator.create()
        prompts_df = prompt_dataset.get_prompts_dataframe(CreationPromptGenerator())
        PromptTestProject.verify_prompts_safa_project(self, prompts_df)

    @mock.patch("openai.Completion.create")
    def verify_summarization(self, mock_completion: mock.MagicMock, dataset_creator, artifacts_entries):
        """
        Verifies that entries are properly summarized by reader
        :return: None
        """
        mock_completion.side_effect = fake_open_ai_completion
        prompt_dataset: PromptDataset = dataset_creator.create()
        for row in artifacts_entries:
            row[ArtifactKeys.CONTENT.value] = SUMMARY_FORMAT.format(row[ArtifactKeys.CONTENT.value])
        artifacts_df = prompt_dataset.artifact_df if prompt_dataset.artifact_df is not None \
            else prompt_dataset.trace_dataset.artifact_df
        TestAssertions.verify_entities_in_df(self, artifacts_entries, artifacts_df)

    def get_prompt_dataset_creator(self, **params):
        return PromptDatasetCreator(**params)
