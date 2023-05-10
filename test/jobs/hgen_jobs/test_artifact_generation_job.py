from unittest import mock

from tgen.data.chunkers.python_chunker import PythonChunker
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.prompts.supported_prompts import SupportedPrompts
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.data_jobs.summarize_artifacts_job import SummarizeArtifactsJob
from tgen.jobs.hgen_jobs.artifact_generator_job import ArtifactGeneratorJob
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.testres.test_open_ai_responses import fake_open_ai_completion
from tgen.train.args.open_ai_args import OpenAIArgs


class TestArtifactGenerationJob(BaseJobTest):
    ARTIFACTS = {"s1": {ArtifactKeys.CONTENT.value: "public class HelloWorld { "
                                                    "public static void main(String[] args) "
                                                    "{ String message = \"Hello, World!\"; "
                                                    "System.out.println(message);}}", SummarizeArtifactsJob.TYPE_KEY: "java"},
                 "s2": {ArtifactKeys.CONTENT.value: "print('Hello, World!')", SummarizeArtifactsJob.TYPE_KEY: "py"},
                 "s3": {ArtifactKeys.CONTENT.value: "content3", SummarizeArtifactsJob.TYPE_KEY: "unknown"}}
    ARTIFACTS_BY_CLUSTER = [["s1", "s2"], ["s3"]]

    @mock.patch("openai.Completion.create")
    @mock.patch.object(OpenAIManager, "make_completion_request_impl", side_effect=fake_open_ai_completion)
    def test_run_success(self, fake_open_ai_completion_mock: mock.MagicMock, mock_completion: mock.MagicMock):
        """
        Tests that job is completed succesfully.
        """
        mock_completion.side_effect = fake_open_ai_completion
        self._test_run_success()

    def _assert_success(self, job: AbstractJob, output_dict: dict):
        self.assertIn(JobResult.BODY, output_dict)
        self.assertEqual(len(output_dict[JobResult.BODY]), len(self.ARTIFACTS_BY_CLUSTER))
        for i, artifact_ids in enumerate(self.ARTIFACTS_BY_CLUSTER):
            for a_id in artifact_ids:
                self.assertIn(self.ARTIFACTS[a_id][ArtifactKeys.CONTENT.value], output_dict[JobResult.BODY][i])

    def _get_job(self) -> AbstractJob:
        llm_manager = OpenAIManager(OpenAIArgs())
        hgen_base_prompt = SupportedPrompts.SYSTEM_REQUIREMENT_CREATION.value
        return ArtifactGeneratorJob(self.ARTIFACTS, self.ARTIFACTS_BY_CLUSTER, llm_manager, hgen_base_prompt)
