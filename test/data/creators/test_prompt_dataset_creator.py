import os

from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.keys.prompt_keys import PromptKeys
from tgen.data.prompts.creation_prompt_generator import CreationPromptGenerator
from tgen.data.readers.prompt_project_reader import PromptProjectReader
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_DATA_DIR
from tgen.testres.testprojects.artifact_test_project import ArtifactTestProject
from tgen.testres.testprojects.safa_test_project import SafaTestProject


class TestPromptDatasetCreator(BaseTest):

    def test_project_reader_artifact(self):
        artifact_project_reader = ArtifactTestProject().get_project_reader()
        dataset_creator = self.get_prompt_dataset_creator(project_reader=artifact_project_reader)
        prompt_dataset = dataset_creator.create()
        prompts_df = prompt_dataset.get_prompts_dataframe(CreationPromptGenerator())
        artifacts = self.get_safa_artifacts()
        self.assertEqual(len(prompts_df), len(artifacts))
        for i, row in prompts_df.iterrows():
            tokens = artifacts[i][ArtifactKeys.CONTENT.value]
            self.assertIn(tokens, row[PromptKeys.PROMPT.value])

    def test_project_reader_prompt(self):
        prompt_project_reader = PromptProjectReader(project_path=os.path.join(TEST_DATA_DIR, "prompt", "safa_proj.jsonl"))
        dataset_creator = self.get_prompt_dataset_creator(project_reader=prompt_project_reader)
        self.verify_dataset_creator(dataset_creator)

    def test_trace_dataset_creator(self):
        project_reader = SafaTestProject().get_project_reader()
        trace_dataset_creator = TraceDatasetCreator(project_reader)
        dataset_creator = self.get_prompt_dataset_creator(trace_dataset_creator=trace_dataset_creator)
        self.verify_dataset_creator(dataset_creator)

    def test_project_file_id(self):
        dataset_creator = self.get_prompt_dataset_creator(project_file_id="id")
        trace_dataset = dataset_creator.create()
        self.assertEqual(trace_dataset.project_file_id, "id")

    def verify_dataset_creator(self, dataset_creator: PromptDatasetCreator):
        prompt_dataset = dataset_creator.create()
        entries = SafaTestProject().get_trace_entries()
        prompt_df = prompt_dataset.get_prompts_dataframe(CreationPromptGenerator())
        prompt_dataset.export_prompt_dataset(prompt_df, os.path.join(TEST_DATA_DIR, "prompt", "safa_proj.jsonl"))
        self.assertEqual(len(entries), len(prompt_df))
        artifacts = {artifact[ArtifactKeys.ID.value]: artifact[ArtifactKeys.CONTENT.value] for artifact in self.get_safa_artifacts()}
        for i, row in prompt_df.iterrows():
            entry = entries[i]
            source_id, target_id = entry[TraceKeys.SOURCE.value], entry[TraceKeys.TARGET.value]
            source, target = artifacts[source_id], artifacts[target_id]
            self.assertIn(target, row[PromptKeys.PROMPT.value])
            self.assertIn(source, row[PromptKeys.COMPLETION.value])

    def get_safa_artifacts(self):
        source_layers = SafaTestProject().get_source_entries()
        target_layers = SafaTestProject().get_target_entries()
        artifacts = []
        for i, layer in enumerate(source_layers):
            artifacts.extend(layer)
            artifacts.extend((target_layers[i]))
        return artifacts

    def get_prompt_dataset_creator(self, **params):
        return PromptDatasetCreator(**params)
