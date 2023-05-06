from unittest import mock

from tgen.data.chunkers.java_chunker import JavaChunker
from tgen.data.chunkers.python_chunker import PythonChunker
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.data_jobs.summarize_artifacts_job import SummarizeArtifactsJob
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.testres.test_open_ai_responses import fake_open_ai_completion
from tgen.util.enum_util import EnumDict


class TestSummarizeJob(BaseJobTest):
    ARTIFACTS = {"s1": {ArtifactKeys.CONTENT.value: "public class HelloWorld { "
                                                    "public static void main(String[] args) "
                                                    "{ String message = \"Hello, World!\"; "
                                                    "System.out.println(message);}}", SummarizeArtifactsJob.TYPE_KEY: "java"},
                 "s2": {ArtifactKeys.CONTENT.value: "print('Hello, World!')", SummarizeArtifactsJob.TYPE_KEY: "py"},
                 "s3": {ArtifactKeys.CONTENT.value: "content3", SummarizeArtifactsJob.TYPE_KEY: "unknown"}}

    @mock.patch.object(PythonChunker, "chunk", side_effect=lambda content, **kwargs: ["python " + content])
    @mock.patch.object(JavaChunker, "chunk",  side_effect=lambda content, **kwargs: ["java " + content])
    @mock.patch.object(OpenAIManager, "make_completion_request_impl", side_effect=fake_open_ai_completion)
    def test_run_success(self, fake_open_ai_completion_mock: mock.MagicMock, fake_java_chunk: mock.MagicMock,
                         fake_python_chunk: mock.MagicMock):
        """
        Tests that job is completed succesfully.
        """
        self._test_run_success()

    def _assert_success(self, job: AbstractJob, output_dict: dict):
        self.assertIn(JobResult.ARTIFACTS, output_dict)
        for artifact_id, artifact in output_dict[JobResult.ARTIFACTS].items():
            artifact = EnumDict(artifact)
            self.assertIn("Summary of ", artifact[ArtifactKeys.CONTENT])
            if self.ARTIFACTS[artifact_id][SummarizeArtifactsJob.TYPE_KEY] == "py":
                self.assertIn("python", artifact[ArtifactKeys.CONTENT])
            elif self.ARTIFACTS[artifact_id][SummarizeArtifactsJob.TYPE_KEY] == "java":
                self.assertIn("java", artifact[ArtifactKeys.CONTENT])
            else:
                self.assertNotIn("python", artifact[ArtifactKeys.CONTENT])
                self.assertNotIn("java", artifact[ArtifactKeys.CONTENT])

    def _get_job(self) -> AbstractJob:
        return SummarizeArtifactsJob(self.ARTIFACTS)
