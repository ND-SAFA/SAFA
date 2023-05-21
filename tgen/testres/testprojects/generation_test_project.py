from typing import List

from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.jobs.data_jobs.summarize_artifacts_job import SummarizeArtifactsJob


class GenerationTestProject:
    """
    Holds data for generating artifacts, summarizing them, and other generation tasks.
    """
    ARTIFACTS = [
        {
            ArtifactKeys.ID.value: "s1",
            ArtifactKeys.CONTENT.value: "public class HelloWorld { "
                                        "public static void main(String[] args) "
                                        "{ String message = \"Hello, World!\"; "
                                        "System.out.println(message);}}",
            SummarizeArtifactsJob.TYPE_KEY: "java"
        },
        {
            ArtifactKeys.ID.value: "s2",
            ArtifactKeys.CONTENT.value: "print('Hello, World!')",
            SummarizeArtifactsJob.TYPE_KEY: "py"},
        {
            ArtifactKeys.ID.value: "s3",
            ArtifactKeys.CONTENT.value: "content3",
            SummarizeArtifactsJob.TYPE_KEY: "unknown"
        }]
    ARTIFACT_MAP = {"s1": 0, "s2": 1, "s3": 2}

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
