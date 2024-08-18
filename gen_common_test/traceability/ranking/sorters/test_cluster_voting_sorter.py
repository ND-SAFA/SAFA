from gen_common.clustering.base.cluster import Cluster
from gen_common.constants.model_constants import DEFAULT_TEST_EMBEDDING_MODEL
from gen_common.traceability.ranking.sorters.cluster_voting_sorter import ClusterVotingSorter
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
    INITIAL_CLUSTERS = {'0': Cluster.from_artifacts(['A2', 'A3', 'P2'], EMBEDDING_MANAGER),
                        '1': Cluster.from_artifacts(['A4', 'P2'], EMBEDDING_MANAGER),
                        '2': Cluster.from_artifacts(['A2', 'A5'], EMBEDDING_MANAGER),
                        '3': Cluster.from_artifacts(['A1', 'A4', 'P1', 'P3'], EMBEDDING_MANAGER),
                        '4': Cluster.from_artifacts(['P1', 'A1'], EMBEDDING_MANAGER),
                        '5': Cluster.from_artifacts(['P2', 'A3'], EMBEDDING_MANAGER)
                        }
    FINAL_CLUSTERS = {k: v for k, v in INITIAL_CLUSTERS.items() if int(k) < 4}
    PARENTS = [a for a in ARTIFACT_MAP.keys() if a.startswith("P")]
    CHILDREN = [a for a in ARTIFACT_MAP.keys() if a.startswith("A")]
    COUNTS = {"P2": {"A2": 1, "A3": 2, "A4": 1},
              "P1": {"A1": 2, "A4": 1},
              "P3": {"A1": 1, "A4": 1}}

    def test_sort(self):
        parent2rankings = ClusterVotingSorter.sort(parent_ids=self.PARENTS, child_ids=self.CHILDREN,
                                                   initial_clusters=self.INITIAL_CLUSTERS,
                                                   final_clusters=self.FINAL_CLUSTERS,
                                                   embedding_manager=self.EMBEDDING_MANAGER)
        for parent, counts in self.COUNTS.items():
            self.assertSetEqual(set(parent2rankings[parent][:len(counts)]), set(counts.keys()))
            self.assertSetEqual(set(parent2rankings[parent]), set(self.CHILDREN))
            for child, count in counts.items():
                if count == 2:
                    self.assertEqual(parent2rankings[parent][0], child)
