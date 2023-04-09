from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.prompts.creation_prompt_generator import CreationPromptGenerator
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.testprojects.prompt_test_project import PromptTestProject


class TestPromptDatasetCreator(BaseTest):

    def test_project_reader_artifact(self):
        artifact_project_reader = PromptTestProject.get_artifact_project_reader()
        dataset_creator = self.get_prompt_dataset_creator(project_reader=artifact_project_reader)
        prompt_dataset = dataset_creator.create()
        prompts_df = prompt_dataset.get_prompts_dataframe(CreationPromptGenerator())
        PromptTestProject.verify_prompts_artifacts_project(self, prompts_df)

    def test_project_reader_prompt(self):
        prompt_project_reader = PromptTestProject.get_project_reader()
        dataset_creator = self.get_prompt_dataset_creator(project_reader=prompt_project_reader)
        self.verify_dataset_creator(dataset_creator)

    def test_trace_dataset_creator(self):
        trace_dataset_creator = PromptTestProject.get_trace_dataset_creator()
        dataset_creator = self.get_prompt_dataset_creator(trace_dataset_creator=trace_dataset_creator)
        self.verify_dataset_creator(dataset_creator)

    def test_project_file_id(self):
        dataset_creator = self.get_prompt_dataset_creator(project_file_id="id")
        trace_dataset = dataset_creator.create()
        self.assertEqual(trace_dataset.project_file_id, "id")

    def verify_dataset_creator(self, dataset_creator: PromptDatasetCreator):
        prompt_dataset = dataset_creator.create()
        prompts_df = prompt_dataset.get_prompts_dataframe(CreationPromptGenerator())
        PromptTestProject.verify_prompts_safa_project(self, prompts_df)

    def get_prompt_dataset_creator(self, **params):
        return PromptDatasetCreator(**params)
