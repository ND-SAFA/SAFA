from unittest import mock

from tgen.data.chunkers.python_chunker import PythonChunker
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.prompts.supported_prompts import SupportedPrompts
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.data_jobs.summarize_artifacts_job import SummarizeArtifactsJob
from tgen.jobs.hgen_jobs.generate_artifacts_job import GenerateArtifactsJob
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.testres.test_open_ai_responses import fake_open_ai_completion
from tgen.train.args.open_ai_args import OpenAIArgs


class TestSingleArtifactGenerationJob(BaseJobTest):
    ARTIFACTS = {"s1": {ArtifactKeys.CONTENT.value: "public class HelloWorld {\n"
                                                    "public static void main(String[] args)\n"
                                                    "{ String message = \"Hello, World!\";\n"
                                                    "System.out.println(message);}}\n", SummarizeArtifactsJob.TYPE_KEY: "java"},
                 "s2": {ArtifactKeys.CONTENT.value: "print('Hello, World!')", SummarizeArtifactsJob.TYPE_KEY: "py"},
                 "s3": {ArtifactKeys.CONTENT.value: "content3", SummarizeArtifactsJob.TYPE_KEY: "unknown"}}
    ARTIFACTS_BY_CLUSTER = [["s1", "s2"], ["s3"]]

    @mock.patch.object(OpenAIManager, "make_completion_request_impl", side_effect=fake_open_ai_completion)
    def test_run_success(self, fake_open_ai_completion_mock: mock.MagicMock):
        """
        Tests that job is completed successfully.
        """
        self._test_run_success()

    def _assert_success(self, job: AbstractJob, job_result: JobResult):
        artifact_content = [artifact[ArtifactKeys.CONTENT] for id_, artifact in job_result.body.artifact_df.itertuples()
                            if artifact[ArtifactKeys.LAYER_ID] != job.SOURCE_LAYER_ID]
        self.assertEqual(len(artifact_content), len(self.ARTIFACTS_BY_CLUSTER))
        for i, artifact_ids in enumerate(self.ARTIFACTS_BY_CLUSTER):
            for a_id in artifact_ids:
                self.assertIn(self.ARTIFACTS[a_id][ArtifactKeys.CONTENT.value], artifact_content[i])

    def _get_job(self) -> AbstractJob:
        llm_manager = OpenAIManager(OpenAIArgs())
        return GenerateArtifactsJob(self.ARTIFACTS, "user_story", llm_manager, self.ARTIFACTS_BY_CLUSTER)
