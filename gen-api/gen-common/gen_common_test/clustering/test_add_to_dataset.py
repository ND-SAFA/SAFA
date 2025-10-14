from unittest import TestCase

from gen_common.clustering.base.clustering_args import ClusteringArgs
from gen_common.clustering.base.clustering_state import ClusteringState
from gen_common.clustering.steps.add_clusters_to_dataset import AddClustersToDataset
from gen_common_test.clustering.clustering_test_util import ClusteringTestUtil


class TestAddToDataset(TestCase):
    def test_use_case(self):
        """
        Tests that cluster artifacts and links are added to the dataset.
        """
        args: ClusteringArgs = ClusteringTestUtil.create_default_args()
        args.create_dataset = True

        state = ClusteringState()
        state.final_cluster_map = {
            0: ["A1", "A2"],
            1: ["A3", "A4"]
        }

        step = AddClustersToDataset()
        step.run(args, state)

        artifact_df = state.cluster_dataset.trace_dataset.artifact_df
        artifact_types = artifact_df.get_artifact_types()
        self.assertIn(args.cluster_artifact_type, artifact_types)

        # Verifies artifacts were added
        cluster_artifacts = artifact_df.get_artifacts_by_type(args.cluster_artifact_type)
        self.assertEqual(2, len(cluster_artifacts))
        self.assertIsNotNone(artifact_df.get_artifact(0))
        self.assertIsNotNone(artifact_df.get_artifact(1))

        # Verifies all trace links were added
        trace_df = state.cluster_dataset.trace_dataset.trace_df
        for c_id, artifact_ids in state.final_cluster_map.items():
            for a_id in artifact_ids:
                cluster_link = trace_df.get_link(source_id=a_id, target_id=c_id)
                self.assertIsNotNone(cluster_link)

        # Verifies that layer id is updated
        layer_df = state.cluster_dataset.trace_dataset.layer_df
        layers = layer_df.as_list()
        self.assertEqual(1, len(layers))
        traced_layer = layers[0]
        self.assertEqual(ClusteringTestUtil.DEFAULT_ARTIFACT_TYPE, traced_layer[0])
        self.assertEqual(args.cluster_artifact_type, traced_layer[1])
