from tgen.data.clustering.SupportedClusteringMethod import SupportedClusteringMethod
from tgen.data.clustering.artifact_clusterer import ArtifactClusterer
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceKeys, TraceDataFrame
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.tdatasets.dataset_role import DatasetRole
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.object_creator import ObjectCreator
from tgen.util.dataframe_util import DataFrameUtil


class TestArtifactClusterer(BaseTest):
    CLUSTERS = {'s1': 0, 's2': 0, 's3': 2, 't1': 0, 't2': 2, 't3': 5, 's4': 3, 's5': 4, 's6': 1, 't4': 3, 't5': 3, 't6': 4}

    def test_get_clusters(self):
        clusterer = self.get_artifact_clusterer()
        for method in SupportedClusteringMethod:
            clusters = clusterer.get_clusters(method)
            self.assertEqual(len(clusters), len(clusterer.trace_dataset.artifact_df))

    def test_create_dataset_from_clusters(self):
        clusterer = self.get_artifact_clusterer()
        for method in SupportedClusteringMethod:
            dataset = clusterer.create_dataset_from_clusters(method)
            self.assertIsInstance(dataset, TraceDataset)

    def test_get_trace_df_from_clusters(self):
        def verify_cluster_link(query_key, query_pair_key):
            artifact_links = DataFrameUtil.query_df(orig_trace_df, {query_key: artifact_id})
            for _, link in artifact_links.iterrows():
                cluster_pair_num = clusters[link[query_pair_key]]
                if cluster_num != cluster_pair_num:
                    cluster_link_id = TraceDataFrame.generate_link_id(cluster_num, cluster_pair_num)
                    if cluster_link_id not in list(cluster_trace_df.index):
                        cluster_link_id = TraceDataFrame.generate_link_id(cluster_pair_num, cluster_num)
                        self.assertIn(cluster_link_id, list(cluster_trace_df.index))
                    self.assertEqual(link[TraceKeys.LABEL.value], cluster_trace_df.get_link(cluster_link_id)[TraceKeys.LABEL])

        orig_trace_df = self.get_trace_dataset().trace_df
        clusters = self.CLUSTERS
        cluster_trace_df = ArtifactClusterer._get_trace_df_from_clusters(clusters, orig_trace_df)
        for artifact_id, cluster_num in clusters.items():
            verify_cluster_link(TraceKeys.SOURCE.value, TraceKeys.TARGET.value)
            verify_cluster_link(TraceKeys.TARGET.value, TraceKeys.SOURCE.value)

    def test_get_artifacts_df_from_clusters(self):
        orig_artifact_df = self.get_trace_dataset().artifact_df
        clusters = self.CLUSTERS
        cluster_artifact_df = ArtifactClusterer._get_artifact_df_from_clusters(clusters, orig_artifact_df, "layer_1")
        self.assertEqual(len(cluster_artifact_df), len(set(clusters.values())))
        for artifact_id, cluster_num in clusters.items():
            self.assertIn(int(cluster_num), list(cluster_artifact_df.index))
            cluster = cluster_artifact_df.get_artifact(cluster_num)
            cluster_content = cluster[ArtifactKeys.CONTENT].split("\n")
            orig_artifact_content = orig_artifact_df.get_artifact(artifact_id)[ArtifactKeys.CONTENT]
            self.assertIn(orig_artifact_content, cluster_content)

    def get_trace_dataset(self) -> TraceDataset:
        dataset_manager = ObjectCreator.create(TrainerDatasetManager)
        return dataset_manager[DatasetRole.TRAIN]

    def get_artifact_clusterer(self) -> ArtifactClusterer:
        dataset = self.get_trace_dataset()
        return ArtifactClusterer(dataset)
