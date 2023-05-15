from tgen.constants.deliminator_constants import NEW_LINE
from tgen.data.creators.clustering.supported_clustering_method import SupportedClusteringMethod
from tgen.data.creators.clustering.cluster_dataset_creator import ClusterDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.layer_dataframe import LayerDataFrame, LayerKeys
from tgen.data.dataframes.trace_dataframe import TraceKeys, TraceDataFrame
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.object_creator import ObjectCreator
from tgen.util.dataframe_util import DataFrameUtil


class TestClusterDatasetCreator(BaseTest):
    ARTIFACT2CLUSTERS = {'s1': 0, 's2': 0, 's3': 2, 't1': 0, 't2': 2, 't3': 5, 's4': 3, 's5': 4, 's6': 1, 't4': 3, 't5': 3, 't6': 4}
    METHOD2CLUSTER = {SupportedClusteringMethod.LOUVAIN: {0: ['s1', 's2', 't1'],
                                                          2: ['s3', 't2'],
                                                          5: ['t3']},
                      SupportedClusteringMethod.THRESHOLD: {3: ['s4', 't6', 't4', 't5'],
                                                            1: ['s6'],
                                                            4: ['s5', 't6']}}

    def test_get_clusters(self):
        clusterer = self.get_artifact_clusterer()
        clusters = clusterer.get_clusters()
        for method, expected_clusters in self.METHOD2CLUSTER.items():
            self.assertIn(method, clusters)

    def test_create_dataset_from_clusters(self):
        clusterer = self.get_artifact_clusterer()
        dataset = clusterer.create()
        self.assertIsInstance(dataset, PromptDataset)

    def test_create_dataset_from_clusters(self):
        cluster_layer_id = "layer_1"
        cluster_dataset: PromptDataset = ClusterDatasetCreator._create_dataset_from_clusters(self.METHOD2CLUSTER,
                                                                                             self.get_trace_dataset(),
                                                                                             cluster_layer_id)
        self.verify_artifact_df(cluster_dataset.trace_dataset.artifact_df)
        self.verify_artifact_df(cluster_dataset.artifact_df, includes_orig_artifact=False)
        self.verify_trace_df(cluster_dataset.trace_dataset.trace_df)
        self.verify_layer_df(cluster_dataset.trace_dataset.layer_df, cluster_layer_id=cluster_layer_id)

    def verify_artifact_df(self, cluster_artifact_df, includes_orig_artifact=True):
        orig_artifact_df = self.get_trace_dataset().artifact_df
        expected_total = len(set(self.ARTIFACT2CLUSTERS.values()))
        if includes_orig_artifact:
            expected_total += len(self.ARTIFACT2CLUSTERS.keys())
        self.assertEqual(len(cluster_artifact_df), expected_total)
        for artifact_id, cluster_num in self.ARTIFACT2CLUSTERS.items():
            self.assertIn(int(cluster_num), list(cluster_artifact_df.index))
            cluster = cluster_artifact_df.get_artifact(cluster_num)
            orig_artifact_content = orig_artifact_df.get_artifact(artifact_id)[ArtifactKeys.CONTENT]
            self.assertIn(orig_artifact_content, cluster[ArtifactKeys.CONTENT])
            if includes_orig_artifact:
                self.assertIn(artifact_id, list(cluster_artifact_df.index))

    def verify_trace_df(self, cluster_trace_df):
        orig_trace_df = self.get_trace_dataset().trace_df
        expected_n_traces = len(orig_trace_df) + (len(self.ARTIFACT2CLUSTERS) * len(set(self.ARTIFACT2CLUSTERS.values())))
        self.assertEqual(expected_n_traces, len(cluster_trace_df))
        for link_id in orig_trace_df.index:
            self.assertIn(link_id, cluster_trace_df)
        for method, clusters in self.METHOD2CLUSTER.items():
            for cluster_id in clusters.keys():
                for artifact_id in self.ARTIFACT2CLUSTERS.keys():
                    link = cluster_trace_df.get_link(source_id=artifact_id, target_id=cluster_id)
                    self.assertIsNotNone(link)
                    if artifact_id in clusters[cluster_id]:
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
        dataset = self.get_trace_dataset()
        return ClusterDatasetCreator(dataset, cluster_methods=set(self.METHOD2CLUSTER.keys()))
