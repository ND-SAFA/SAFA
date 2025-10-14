from gen_common.clustering.base.cluster import Cluster
from gen_common.constants.model_constants import DEFAULT_TEST_EMBEDDING_MODEL
from gen_common.traceability.ranking.sorters.cluster_children_sorter import ClusterChildrenSorter
from gen_common.traceability.relationship_manager.embeddings_manager import EmbeddingsManager
from gen_common_test.base.tests.base_test import BaseTest


class TestClusterChildrenSorter(BaseTest):
    ARTIFACT_MAP = {
        "A1": "Doggies are really cute.",
        "A2": "Car goes vroom.",
        "A3": "Fire trucks are really loud.",
        "A4": "Dogs pee on fire hydrants.",
        "A5": "The street is noisy.",
        "P1": "Some people have cats as pets.",
        "P2": "That house is on fire.",
        "P3": "Zebras are at the zoo."
    }
    EMBEDDING_MANAGER = EmbeddingsManager(ARTIFACT_MAP, DEFAULT_TEST_EMBEDDING_MODEL)
    CLUSTERS = {'0': Cluster.from_artifacts(['A2', 'A3'], EMBEDDING_MANAGER),
                '1': Cluster.from_artifacts(['A1', 'A4'], EMBEDDING_MANAGER),
                '2': Cluster.from_artifacts(['A2', 'A5'], EMBEDDING_MANAGER)}
    PARENTS = [a for a in ARTIFACT_MAP.keys() if a.startswith("P")]
    CHILDREN = [a for a in ARTIFACT_MAP.keys() if a.startswith("A")]
    EXPECTED_PARENT_TO_CLUSTER = {"P1": "1", "P2": "0", "P3": "1"}

    def test_sort(self):
        parent2rankings = ClusterChildrenSorter.sort(parent_ids=self.PARENTS, child_ids=self.CHILDREN, final_clusters=self.CLUSTERS,
                                                     embedding_manager=self.EMBEDDING_MANAGER)
        for parent, rankings in parent2rankings.items():
            self.assertSetEqual(set(rankings), set(self.CHILDREN))
            best_artifacts = self.CLUSTERS[self.EXPECTED_PARENT_TO_CLUSTER[parent]].artifact_ids
            self.assertEqual(set(rankings[:len(best_artifacts)]), set(best_artifacts))
