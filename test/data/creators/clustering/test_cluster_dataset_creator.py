from collections import namedtuple
from unittest import mock

from tgen.data.creators.cluster_dataset_creator import ClusterDatasetCreator
from tgen.data.clustering.supported_clustering_method import SupportedClusteringMethod
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerDataFrame, LayerKeys
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.llm_responses import GenerationResponse
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.object_creator import ObjectCreator


class TestClusterDatasetCreator(BaseTest):
    ARTIFACT2CLUSTERS = {'s1': 0, 's2': 0, 's3': 2, 't1': 0, 't2': 2, 't3': 5, 's4': 3, 's5': 4, 's6': 1, 't4': 3, 't5': 3, 't6': 4}
    METHOD2CLUSTER = {SupportedClusteringMethod.GRAPH: {0: ['s1', 's2', 't1'],
                                                        2: ['s3', 't2'],
                                                        5: ['t3']},
                      SupportedClusteringMethod.LLM: {3: ['s4', 't4', 't5'],
                                                      1: ['s6'],
                                                      4: ['s5', 't6']}}

    res = GenerationResponse(batch_responses=['<group>\n<summary>3</summary>\n'
                                              '<artifacts>6,9,10</artifacts>\n</group>\n\n<group>\n<summary>1</summary>\
                                              n<artifacts>8</artifacts> \n</group>\n\n<group>\n'
                                              '<summary>4</summary>\n<artifacts>7,11</artifacts> \n</group>'])

    @mock.patch.object(AbstractLLMManager, "make_completion_request")
    def test_get_clusters(self, completion_request_mock: mock.MagicMock):
        completion_request_mock.return_value = self.res
        clusterer = self.get_artifact_clusterer()
        clusters = clusterer.get_clusters()
        self.assertIn(SupportedClusteringMethod.GRAPH, clusters)

    @mock.patch.object(AbstractLLMManager, "make_completion_request")
    @mock.patch("cdlib.algorithms.louvain")
    def test_create(self, louvain_mock: mock.MagicMock, completion_request_mock: mock.MagicMock):
        Louvain = namedtuple("Louvain", ["communities"])
        louvain_mock.return_value = Louvain(communities=self.METHOD2CLUSTER[SupportedClusteringMethod.GRAPH].values())
        completion_request_mock.return_value = self.res
        clusterer = self.get_artifact_clusterer()
        cluster_dataset: PromptDataset = clusterer.create()
        cluster_id_to_num, cluster_num_to_id = self._get_cluster_id_to_num_mapping(cluster_dataset.artifact_df)
        self.verify_artifact_df(cluster_dataset.artifact_df, cluster_id_to_num, includes_orig_artifact=False)
        self.verify_artifact_df(cluster_dataset.trace_dataset.artifact_df, cluster_id_to_num, includes_orig_artifact=True)
        self.verify_trace_df(cluster_dataset.trace_dataset.trace_df, cluster_num_to_id)
        self.verify_layer_df(cluster_dataset.trace_dataset.layer_df, cluster_layer_id=clusterer.layer_id)

    def _get_cluster_id_to_num_mapping(self, cluster_artifact_df):
        orig_artifact_df = self.get_trace_dataset().artifact_df
        id2num = {}
        num2id = {}
        for cluster_id, cluster in cluster_artifact_df.itertuples():
            cluster_num = None
            for artifact_id, artifact in orig_artifact_df.itertuples():
                if artifact[ArtifactKeys.CONTENT] in cluster[ArtifactKeys.CONTENT]:
                    cluster_num = self.ARTIFACT2CLUSTERS[artifact_id]
                    break
            id2num[cluster_id] = cluster_num
            num2id[cluster_num] = cluster_id
            self.assertIsNotNone(cluster_num)
        return id2num, num2id

    def verify_artifact_df(self, cluster_artifact_df, cluster_id_to_num, includes_orig_artifact=True):
        orig_artifact_df = self.get_trace_dataset().artifact_df
        expected_total = len(set(self.ARTIFACT2CLUSTERS.values()))
        if includes_orig_artifact:
            expected_total += len(self.ARTIFACT2CLUSTERS.keys())
        self.assertEqual(len(cluster_artifact_df), expected_total)
        for cluster_id, cluster in cluster_artifact_df.itertuples():
            if cluster_id in orig_artifact_df:
                continue
            cluster_num = cluster_id_to_num[cluster_id]
            expected_cluster = self.METHOD2CLUSTER[SupportedClusteringMethod.GRAPH][cluster_num] \
                if cluster_num in self.METHOD2CLUSTER[SupportedClusteringMethod.GRAPH] else \
            self.METHOD2CLUSTER[SupportedClusteringMethod.LLM][cluster_num]
            for artifact_id in expected_cluster:
                self.assertIn(orig_artifact_df.get_artifact(artifact_id)[ArtifactKeys.CONTENT], cluster[ArtifactKeys.CONTENT])

    def verify_trace_df(self, cluster_trace_df, cluster_num_to_id):
        orig_trace_df = self.get_trace_dataset().trace_df
        expected_n_traces = len(orig_trace_df) + (len(self.ARTIFACT2CLUSTERS) * len(set(self.ARTIFACT2CLUSTERS.values())))
        self.assertEqual(expected_n_traces, len(cluster_trace_df))
        for link_id in orig_trace_df.index:
            self.assertIn(link_id, cluster_trace_df)
        for method, clusters in self.METHOD2CLUSTER.items():
            for cluster_num in clusters.keys():
                for artifact_id in self.ARTIFACT2CLUSTERS.keys():
                    cluster_id = cluster_num_to_id[cluster_num]
                    link = cluster_trace_df.get_link(source_id=artifact_id, target_id=cluster_id)
                    self.assertIsNotNone(link)
                    if artifact_id in clusters[cluster_num]:
                        self.assertEqual(link[TraceKeys.LABEL], 1)
                    else:
                        self.assertEqual(link[TraceKeys.LABEL], 0)

    def verify_layer_df(self, cluster_layer_df: LayerDataFrame, cluster_layer_id):
        trace_dataset = self.get_trace_dataset()
        orig_layer_df = trace_dataset.layer_df
        orig_artifact_df = trace_dataset.artifact_df
        for i, layer in orig_layer_df.itertuples():
            query = cluster_layer_df.filter_by_row(lambda row: row[LayerKeys.SOURCE_TYPE.value] == layer[LayerKeys.SOURCE_TYPE]
                                                               and row[LayerKeys.TARGET_TYPE.value] == layer[LayerKeys.TARGET_TYPE])
            self.assertEqual(len(query), 1)
        artifact_layers = set()
        for artifact_id in self.ARTIFACT2CLUSTERS.keys():
            artifact_layer_id = orig_artifact_df.get_artifact(artifact_id)[ArtifactKeys.LAYER_ID]
            artifact_layers.add(artifact_layer_id)
            query = cluster_layer_df.filter_by_row(lambda row: row[LayerKeys.SOURCE_TYPE.value] == artifact_layer_id
                                                               and row[LayerKeys.TARGET_TYPE.value] == cluster_layer_id)
            self.assertEqual(len(query), 1)
        expected_n_layers = len(artifact_layers) + len(orig_layer_df.index)
        self.assertEqual(len(cluster_layer_df), expected_n_layers)

    def get_trace_dataset(self) -> TraceDataset:
        dataset_manager = ObjectCreator.create(TrainerDatasetManager)
        return dataset_manager[DatasetRole.TRAIN]

    def get_artifact_clusterer(self) -> ClusterDatasetCreator:
        dataset = PromptDataset(trace_dataset=self.get_trace_dataset())
        return ClusterDatasetCreator(dataset, cluster_methods={SupportedClusteringMethod.GRAPH, SupportedClusteringMethod.LLM})
