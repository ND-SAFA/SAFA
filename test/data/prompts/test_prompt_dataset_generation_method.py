from tgen.core.args.open_ai_args import OpenAIArgs
from tgen.data.prompts.prompt_builder import PromptBuilder
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.testprojects.prompt_test_project import PromptTestProject


class TestResponse:
    id = "id_from_res"


class TestPromptDataset(BaseTest):


    def test_get_generation_method(self):
        llm_manager = OpenAIManager(OpenAIArgs())
        prompt_builder = PromptBuilder([])

        # Verify builder config
        config = prompt_builder.config
        self.assertFalse(config.requires_trace_per_prompt)
        self.assertFalse(config.requires_artifact_per_prompt)
        self.assertFalse(config.requires_all_artifacts)

        # Verify generation method
        artifact_prompt_dataset: PromptDataset = self.get_prompt_dataset_from_artifact_df()
        generation_method = artifact_prompt_dataset._get_generation_method(llm_manager.prompt_args, prompt_builder)
        print("hi")

    @staticmethod
    def get_prompt_dataset_from_artifact_df() -> PromptDataset:
        artifact_project_reader = PromptTestProject.get_artifact_project_reader()
        artifacts_df = artifact_project_reader.read_project()
        return PromptDataset(artifact_df=artifacts_df)
