from unittest import mock
from unittest.mock import MagicMock

from gen_common.constants.model_constants import DEFAULT_TEST_EMBEDDING_MODEL
from gen_common.data.creators.prompt_dataset_creator import PromptDatasetCreator
from gen_common.data.creators.trace_dataset_creator import TraceDatasetCreator
from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.jobs.job_args import JobArgs
from gen_common.summarize.project.project_summarizer import ProjectSummarizer
from gen_common.traceability.ranking.job import RankingJob
from gen_common.traceability.ranking.supported_ranking_pipelines import SupportedRankingPipelines
from gen_common.util.status import Status
from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.tests.base_test import BaseTest
from gen_common_test.test_data.test_data_manager import TestDataManager
from gen_common_test.traceability.ranking.steps.ranking_pipeline_test import RankingPipelineTest


class TestRankingJob(BaseTest):
    """
    Tests the module requirements: https://www.notion.so/nd-safa/ranking_job-01aa9f2c32fc40ef96227789c3d999e7?pvs=4
    """

    def test_data_inputs(self):
        self.assert_error(lambda: RankingJob(JobArgs()), AssertionError, "Must supply either a dataset or a creator to make one.")
        self.assert_error(lambda: RankingJob(JobArgs(dataset_creator=1, dataset=1)), AssertionError,
                          "Must provide only a dataset OR a dataset creator")
        self.assert_error(lambda: RankingJob(JobArgs(dataset=PromptDataset(artifact_df=ArtifactDataFrame()))), AssertionError,
                          "Must specify parent-child layers or provide trace dataset")

    def test_accept_custom_ranking_args(self):
        job = self.create_job(max_context_artifacts=20)
        self.assertIn("max_context_artifacts", job.ranking_kwargs)

    def test_multi_layer_tracing_requests(self):
        job = self.create_job()
        tracing_types = job.job_args.dataset.trace_dataset.get_parent_child_types()
        self.assertEqual(2, len(tracing_types))
        for i, (parent_type, child_type) in enumerate(tracing_types):
            self.assertEqual(f"source_{i + 1}", child_type)
            self.assertEqual(f"target_{i + 1}", parent_type)

    @mock.patch.object(ProjectSummarizer, "summarize")
    @mock_anthropic
    def test_non_default_ranking_pipeline(self, anthropic_ai_manager: TestAIManager, project_summarizer_mock: MagicMock):
        anthropic_ai_manager.mock_summarization()
        anthropic_ai_manager.set_responses([RankingPipelineTest.get_response()
                                            for _ in range(TestDataManager.get_n_candidates())])
        job = self.create_job_using_embeddings(select_top_predictions=False)
        job_result = job.run()
        self.assertEqual(Status.SUCCESS, job_result.status)
        prediction_entries = job_result.body.prediction_entries
        self.assertEqual(len(prediction_entries), TestDataManager.get_n_candidates())

    def create_job_using_embeddings(self, **kwargs):
        job = self.create_job(ranking_pipeline=SupportedRankingPipelines.EMBEDDING,
                              embedding_model_name=DEFAULT_TEST_EMBEDDING_MODEL,
                              generate_explanations=True, **kwargs)
        return job

    @staticmethod
    def create_job(**kwargs):
        project_reader = TestDataManager.get_project_reader()
        project_creator = PromptDatasetCreator(trace_dataset_creator=TraceDatasetCreator(project_reader=project_reader))
        job = RankingJob(JobArgs(dataset_creator=project_creator), **kwargs)
        return job
