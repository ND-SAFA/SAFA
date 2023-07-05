from unittest import mock, skip

from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.job_result import JobResult
from tgen.jobs.hgen_jobs.generate_artifacts_job import GenerateArtifactsJob
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.testres.base_tests.base_job_test import BaseJobTest
from tgen.testres.test_open_ai_responses import fake_open_ai_completion
from tgen.testres.testprojects.generation_test_project import GenerationTestProject
from tgen.train.args.open_ai_args import OpenAIArgs

@skip("Skipping hgen tests until can fix for update")
class TestLayerArtifactGenerationJob(BaseJobTest):
    project = GenerationTestProject()
    res = [{"completion": '<group>\n<feature>functionality 1</feature>\n'
                          '<artifacts>0,1</artifacts>\n</group>\n\n<group>\n<feature>functionality 2</feature>'
                          '\n<artifacts>2,3</artifacts> \n</group>\n'}]

    CLUSTERS = {"functionality 1": ["s1", "s2"], "functionality 2": ["s3", "s4"]}

    @mock.patch.object(AnthropicManager, "make_completion_request_impl", return_value=res)
    @mock.patch.object(OpenAIManager, "make_completion_request_impl", side_effect=fake_open_ai_completion)
    def test_run_success(self, fake_open_ai_completion_mock: mock.MagicMock, fake_anthropic_completion_mock: mock.MagicMock):
        """
        Tests that job is completed succesfully.
        """
        self._test_run_success()

    def _assert_success(self, job: AbstractJob, job_result: JobResult):
        dataset: TraceDataset = job_result.body
        artifact_ids = self.project.get_artifact_ids()
        all_artifacts = artifact_ids + list(self.CLUSTERS.keys())
        self.assertSize(len(all_artifacts), dataset.artifact_df)
        for artifact_id in all_artifacts:
            self.assertIn(artifact_id, dataset.artifact_df)
        self.assertSize(len(self.project.ARTIFACTS) * len(self.CLUSTERS), dataset.trace_df)
        for cluster_id, artifacts in self.CLUSTERS.items():
            for artifact_id in artifacts:
                self.assertIsNotNone(dataset.trace_df.get_link(source_id=artifact_id, target_id=cluster_id))

    def _get_job(self) -> AbstractJob:
        return GenerateArtifactsJob(self.project.ARTIFACTS, "user_story", hgen_llm_manager=OpenAIManager())
