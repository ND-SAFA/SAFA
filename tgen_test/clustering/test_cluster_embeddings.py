from unittest import TestCase

from tgen_test.clustering.clustering_test_util import ClusteringTestUtil
from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.steps.create_clusters_from_embeddings import CreateClustersFromEmbeddings
from tgen.clustering.steps.create_embeddings import CreateEmbeddings


class TestClusterEmbeddings(TestCase):
    def test_use_case(self):
        """
        Tests that multiple algorithms are used to create clusters for artifacts.
        """
        artifact_map = {
            "A1": "Doggies are really cute.",
            "A2": "Car goes vroom.",
            "A3": "Fire trucks are really loud.",
            "A4": "Dogs pee on fire hydrants."
        }
        artifacts = list(artifact_map.values())

        state = ClusteringState()
        args = ClusteringTestUtil.create_clustering_args(artifacts)

        CreateEmbeddings().run(args, state)
        CreateClustersFromEmbeddings().run(args, state)

        cluster_map = state.final_cluster_map

        ClusteringTestUtil.verify_clusters(self, cluster_map, {
            "0:0": ["A1", "A4"],
            "0:1": ["A2", "A3"]
        })

    def test_condense_clusters(self):
        """
        Tests that cluster are condensed based on their similarity.
        """
        args = ClusteringTestUtil.create_clustering_args(["hi"])  # artifacts are required, but ignored.
        state = ClusteringState()

        args.cluster_min_votes = 1
        args.cluster_intersection_threshold = 0.8

        step = CreateClustersFromEmbeddings()
        embeddings_manager = ClusteringTestUtil.create_embeddings_manager()
        c1: Cluster = Cluster.from_artifacts(["A", "B", "C", "D"], embeddings_manager)
        c2: Cluster = Cluster.from_artifacts(["A", "B"], embeddings_manager)
        c3: Cluster = Cluster.from_artifacts(["A"], embeddings_manager)
        batch_cluster_Map = {
            "kmeans0": c1,
            "kmeans2": c2,
            "kmeans3": c3,
            "agglomerative0": Cluster.from_artifacts(["A", "B", "C"], embeddings_manager)
        }

        cluster_map = step.condense_clusters(args, state.embedding_manager, batch_cluster_Map)
        ClusteringTestUtil.assert_contains_clusters(cluster_map, [c1, c2, c3])
