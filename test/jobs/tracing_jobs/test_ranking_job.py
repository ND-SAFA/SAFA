from tgen.common.util.status import Status
from tgen.constants.hugging_face_constants import SMALL_EMBEDDING_MODEL
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.jobs.tracing_jobs.ranking_job import RankingJob
from tgen.ranking.supported_ranking_pipelines import SupportedRankingPipelines
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.test_data_manager import TestDataManager


class TestRankingJob(BaseTest):
    """
    Tests the module requirements: https://www.notion.so/nd-safa/ranking_job-01aa9f2c32fc40ef96227789c3d999e7?pvs=4
    """

    def test_data_inputs(self):
        self.assert_error(lambda: RankingJob(), AssertionError, "Missing required")
        self.assert_error(lambda: RankingJob(dataset_creator=1, artifact_df=1), AssertionError, "Expected only")

    def test_accept_custom_ranking_args(self):
        job = self.create_job(max_context_artifacts=20)
        self.assertIn("max_context_artifacts", job.ranking_kwargs)

    def test_multi_layer_tracing_requests(self):
        job = self.create_job()
        tracing_types, artifact_df, dataset = job.construct_tracing_request()
        self.assertEqual(2, len(tracing_types))
        for i, (parent_type, child_type) in enumerate(tracing_types):
            self.assertEqual(f"source_{i + 1}", child_type)
            self.assertEqual(f"target_{i + 1}", parent_type)

    def test_non_default_ranking_pipeline(self):
        job = self.create_job_using_embeddings(select_top_predictions=False)
        job_result = job.run()
        self.assertEqual(Status.SUCCESS, job_result.status)
        prediction_entries = job_result.body.prediction_entries
        self.assertEqual(len(prediction_entries), TestDataManager.get_n_candidates())

    def create_job_using_embeddings(self, **kwargs):
        job = self.create_job(ranking_pipeline=SupportedRankingPipelines.EMBEDDING,
                              embedding_model=SMALL_EMBEDDING_MODEL, **kwargs)
        return job

    @staticmethod
    def create_job(**kwargs):
        project_reader = TestDataManager.get_project_reader()
        project_creator = TraceDatasetCreator(project_reader=project_reader)
        job = RankingJob(dataset_creator=project_creator, **kwargs)
        return job
