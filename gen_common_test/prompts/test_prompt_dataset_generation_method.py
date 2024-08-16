from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common_test.base_tests.base_test import BaseTest
from gen_common_test.testprojects.prompt_test_project import PromptTestProject


class TestResponse:
    id = "id_from_res"


class TestPromptDataset(BaseTest):

    @staticmethod
    def get_prompt_dataset_from_artifact_df() -> PromptDataset:
        artifact_project_reader = PromptTestProject.get_artifact_project_reader()
        artifact_df = artifact_project_reader.read_project()
        return PromptDataset(artifact_df=artifact_df)
