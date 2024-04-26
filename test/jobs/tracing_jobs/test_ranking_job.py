from unittest import mock
from unittest.mock import MagicMock

from test.ranking.steps.ranking_pipeline_test import RankingPipelineTest
from tgen.common.constants.ranking_constants import DEFAULT_SEARCH_EMBEDDING_MODEL
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.status import Status
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.tracing_jobs.ranking_job import RankingJob
from tgen.summarizer.project.project_summarizer import ProjectSummarizer
from tgen.summarizer.summary import Summary
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager
from tgen.testres.test_data_manager import TestDataManager
from tgen.tracing.ranking.supported_ranking_pipelines import SupportedRankingPipelines


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
        project_summarizer_mock.return_value = Summary(overview=EnumDict({"chunks": ["summary of project"],
                                                                          "title": "overview"}))
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
                              embedding_model_name=DEFAULT_SEARCH_EMBEDDING_MODEL, **kwargs)
        return job

    @staticmethod
    def create_job(**kwargs):
        project_reader = TestDataManager.get_project_reader()
        project_creator = PromptDatasetCreator(trace_dataset_creator=TraceDatasetCreator(project_reader=project_reader))
        job = RankingJob(JobArgs(dataset_creator=project_creator), **kwargs)
        return job
