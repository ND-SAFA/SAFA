from unittest import mock

from bs4 import BeautifulSoup

from tgen.data.clustering.llm_clustering import LLMClustering
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.llm_responses import GenerationResponse
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.models.llm.token_limits import ModelTokenLimits
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.testprojects.artifact_test_project import ArtifactTestProject
from tgen.train.args.anthropic_args import AnthropicArgs
from tgen.train.args.open_ai_args import OpenAIArgs


class TestLLMClustering(BaseTest):
    res = GenerationResponse(batch_responses=['<group>\n<feature>Air lease and arm/disarm functionality</feature>\n'
                                              '<artifacts>0,1,11</artifacts>\n</group>\n\n<group>\n<feature>Circular flight path '
                                              'functionality</feature>\n<artifacts>2,5,9</artifacts> \n</group>\n\n<group>\n'
                                              '<feature>Travel and hover flight path functionality</feature>'
                                              '\n<artifacts>3,10,8</artifacts> \n</group>\n\n<group> \n<feature>Waypoint flight '
                                              'path functionality</feature>\n<artifacts>4,7,6</artifacts>\n</group>'])
    expected_clusters = {'Air lease and arm/disarm functionality': ['s1', 's2', 't6'],
                         'Circular flight path functionality': ['s3', 't3', 't4'],
                         'Travel and hover flight path functionality': ['t1', 't5', 's6'],
                         'Waypoint flight path functionality': ['t2', 's5', 's4']}
    artifact_df = ArtifactTestProject().get_project_reader().read_project()

    @mock.patch.object(AbstractLLMManager, "make_completion_request")
    def test_cluster(self, mock_completion_request: mock.MagicMock):
        mock_completion_request.return_value = self.res
        trace_dataset = TraceDataset(self.artifact_df, TraceDataFrame(), LayerDataFrame())
        clusters = LLMClustering.cluster(trace_dataset,
                                         AnthropicManager(AnthropicArgs()))
        self.assertDictEqual(clusters, self.expected_clusters)

    def test_get_clusters_from_response(self):
        clusters = LLMClustering._get_clusters_from_response(self.res.batch_responses[0], list(self.artifact_df.index))
        self.assertDictEqual(self.expected_clusters, clusters)

        missing_art_res = GenerationResponse(batch_responses=['<group>\n<feature>Air lease and arm/disarm functionality</feature>\n'
                                                              '<artifacts>0,1,11</artifacts>\n</group>\n\n<group>\
                                                              n<feature>Circular flight path functionality</feature>\n \n</group>'])
        missing_artifacts_cluster = LLMClustering._get_clusters_from_response(missing_art_res.batch_responses[0], list(self.artifact_df.index))
        self.assertIn('Air lease and arm/disarm functionality', missing_artifacts_cluster)
        self.assertNotIn('Circular flight path functionality', missing_artifacts_cluster)

        bad_res = GenerationResponse(batch_responses=['Claude is dumb sometimes'])
        bad_res_clusters = LLMClustering._get_clusters_from_response(bad_res.batch_responses[0], self.artifact_df)
        self.assertSize(0, bad_res_clusters)

    def test_get_cluster_name_and_artifacts(self):
        artifact_ids = list(self.artifact_df.index)
        groups = BeautifulSoup(self.res.batch_responses[0], features="lxml").findAll(LLMClustering.CLUSTER_TAG)
        cluster_name_, artifacts = LLMClustering._get_cluster_name_and_artifacts(groups[0], artifact_ids)
        self.assertEqual("Air lease and arm/disarm functionality", cluster_name_)
        self.assertListEqual(artifacts, [artifact_ids[0], artifact_ids[1], artifact_ids[11]])

        bad_group_empty = BeautifulSoup('<group>\n<feature>Air lease and arm/disarm functionality</feature>'
                                        '\n<artifacts></artifacts>\n</group>', features="lxml").find(LLMClustering.CLUSTER_TAG)
        cluster_name_, artifacts = LLMClustering._get_cluster_name_and_artifacts(bad_group_empty, artifact_ids)
        self.assertSize(0, artifacts)

        bad_group_format = BeautifulSoup('<group>\n<feature>Air lease and arm/disarm functionality</feature>'
                                         '\n<artifacts>Claude is dumb sometimes</artifacts>\n</group>', features="lxml") \
            .find(LLMClustering.CLUSTER_TAG)
        cluster_name_, artifacts = LLMClustering._get_cluster_name_and_artifacts(bad_group_format, artifact_ids)
        self.assertSize(0, artifacts)

    def test_get_artifact_id_from_num(self):
        artifact_id = LLMClustering._get_artifact_id_by_num("1", list(self.artifact_df.index))
        self.assertEqual(artifact_id, 's2')

        bad_artifact_id_str = LLMClustering._get_artifact_id_by_num("one", list(self.artifact_df.index))
        self.assertIsNone(bad_artifact_id_str)

        bad_artifact_id_oor = LLMClustering._get_artifact_id_by_num("100", list(self.artifact_df.index))
        self.assertIsNone(bad_artifact_id_oor)

    def test_set_max_tokens(self):
        prompt = "This is a prompt"
        max_tokens = LLMClustering._set_max_tokens(AnthropicManager(), prompt=prompt)
        self.assertEqual(max_tokens, LLMClustering.PERC_TOKENS_FOR_RES*ModelTokenLimits.get_token_limit_for_model("claude"))

        prompt = "This is a prompt"
        max_tokens = LLMClustering._set_max_tokens(OpenAIManager(OpenAIArgs(model="davincci")), prompt=prompt)
        self.assertEqual(max_tokens, LLMClustering.RES_TOKENS_MIN)
