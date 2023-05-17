from collections import namedtuple
from unittest import mock

from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.data_jobs.summarize_artifacts_job import SummarizeArtifactsJob
from tgen.jobs.hgen_jobs.artifact_generator_job import GenerateArtifactsJob
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.testres.test_open_ai_responses import fake_open_ai_completion
from tgen.train.args.open_ai_args import OpenAIArgs


class TestLayerArtifactGenerationJob(BaseJobTest):
    res = [{"completion": '<group>\n<summary>functionality 1</summary>\n'
                          '<artifacts>0,1</artifacts>\n</group>\n\n<group>\n<summary>functionality 2</summary>'
                          '\n<artifacts>2</artifacts> \n</group>\n'}]
    ARTIFACTS = {"s1": {ArtifactKeys.CONTENT.value: "public class HelloWorld {\n"
                                                    "public static void main(String[] args)\n"
                                                    "{ String message = \"Hello, World!\";\n"
                                                    "System.out.println(message);}}\n", SummarizeArtifactsJob.TYPE_KEY: "java"},
                 "s2": {ArtifactKeys.CONTENT.value: "print('Hello, World!')", SummarizeArtifactsJob.TYPE_KEY: "py"},
                 "s3": {ArtifactKeys.CONTENT.value: "content3", SummarizeArtifactsJob.TYPE_KEY: "unknown"}}
    CLUSTERS = {"functionality 1": ["s1", "s2"], "functionality 2": ["s3"]}

    @mock.patch.object(AnthropicManager, "make_completion_request_impl", return_value=res)
    @mock.patch.object(OpenAIManager, "make_completion_request_impl", side_effect=fake_open_ai_completion)
    def test_run_success(self, fake_open_ai_completion_mock: mock.MagicMock, fake_anthropic_completion_mock: mock.MagicMock):
        """
        Tests that job is completed succesfully.
        """
        self._test_run_success()

    def _assert_success(self, job: AbstractJob, job_result: JobResult):
        dataset: TraceDataset = job_result.body
        all_artifacts = list(self.ARTIFACTS.keys()) + list(self.CLUSTERS.keys())
        self.assertSize(len(all_artifacts), dataset.artifact_df)
        for artifact_id in all_artifacts:
            self.assertIn(artifact_id, dataset.artifact_df)
        self.assertSize(len(self.ARTIFACTS)*len(self.CLUSTERS), dataset.trace_df)
        for cluster_id, artifacts in self.CLUSTERS.items():
            for artifact_id in artifacts:
                self.assertIsNotNone(dataset.trace_df.get_link(source_id=artifact_id, target_id=cluster_id))

    def _get_job(self) -> AbstractJob:
        llm_manager = OpenAIManager(OpenAIArgs())
        return GenerateArtifactsJob(self.ARTIFACTS, "user_story", llm_manager)
