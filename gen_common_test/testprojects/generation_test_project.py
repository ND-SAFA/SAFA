from typing import List

from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.data.tdatasets.prompt_dataset import PromptDataset


class GenerationTestProject:
    """
    Holds data for generating artifacts, summarizing them, and other generation tasks.
    """
    ARTIFACTS = [
        {
            ArtifactKeys.ID.value: "file.java",
            ArtifactKeys.CONTENT.value: "public class HelloWorld { "
                                        "public static void main(String[] args) "
                                        "{ String message = \"Hello, World!\"; "
                                        "System.out.println(message);}}",
            ArtifactKeys.LAYER_ID.value: "java"
        },
        {
            ArtifactKeys.ID.value: "file.py",
            ArtifactKeys.CONTENT.value: "print('Hello, World!')",
            ArtifactKeys.LAYER_ID.value: "py"
        },
        {
            ArtifactKeys.ID.value: "s3",
            ArtifactKeys.CONTENT.value: "content3",
            ArtifactKeys.LAYER_ID.value: "unknown"
        },
        {
            ArtifactKeys.ID.value: "s4",
            ArtifactKeys.CONTENT.value: "content4",
            ArtifactKeys.LAYER_ID.value: "nl"
        }
    ]
    ARTIFACT_MAP = {"file.java": 0, "file.py": 1, "s3": 2, "s4": 3}

    def get_dataset(self) -> PromptDataset:
        return PromptDataset(artifact_df=ArtifactDataFrame(self.ARTIFACTS))

    @staticmethod
    def get_artifact(artifact_id: str):
        """
        Returns the artifact with given id.
        :param artifact_id: The artifact id.
        :return: The artifact with given id.
        """
        artifact_index = GenerationTestProject.ARTIFACT_MAP[artifact_id]
        return GenerationTestProject.ARTIFACTS[artifact_index]

    @staticmethod
    def get_artifact_ids() -> List[str]:
        """
        :return: Returns the artifact ids of artifacts.
        """
        return [a[ArtifactKeys.ID.value] for a in GenerationTestProject.ARTIFACTS]
