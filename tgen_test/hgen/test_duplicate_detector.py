import math
import string

from common_resources.tools.util.dict_util import DictUtil
from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.keys.structure_keys import ArtifactKeys
from tgen.hgen.common.duplicate_detector import DuplicateDetector, DuplicateType
from tgen.testres.base_tests.base_test import BaseTest


class TestDuplicateDetector(BaseTest):

    def test_identify_duplicates_from_same_cluster(self):
        artifact_map, cluster_to_contents, duplicate_map, artifact_df = self.get_duplicate_information()
        same_cluster_dups = DuplicateDetector.identify_duplicates_from_same_cluster(duplicate_map, cluster_to_contents, artifact_df)
        self.assertEqual(len(same_cluster_dups), len(cluster_to_contents))  # both og clusters have dups
        for c_id, artifacts in same_cluster_dups.items():
            self.assertEqual(len(artifacts), 2)  # 2 artifacts from each cluster are duplicated
            for a_id in artifacts:
                self.assertIn(artifact_map[a_id], cluster_to_contents[c_id])
                self.assertTrue(any([a_id2 in duplicate_map[a_id] for a_id2 in artifacts if a_id2 != a_id]))

        intra_cluster_dups, _ = DuplicateDetector._remove_dups_not_of_duplicate_type(set(artifact_map.keys()), duplicate_map,
                                                                                     DuplicateType.INTRA_CLUSTER, artifact_df,
                                                                                     original_clusters_to_contents=cluster_to_contents)
        a_id_to_cluster_id = DictUtil.flip(same_cluster_dups)
        for a_id, dups in intra_cluster_dups.items():
            self.assertTrue(all([a_id_to_cluster_id[d] == a_id_to_cluster_id[a_id] for d in dups]))

        inter_cluster_dups, _ = DuplicateDetector._remove_dups_not_of_duplicate_type(set(artifact_map.keys()), duplicate_map,
                                                                                     DuplicateType.INTER_CLUSTER, artifact_df,
                                                                                     original_clusters_to_contents=cluster_to_contents)
        for a_id, dups in inter_cluster_dups.items():
            if a_id not in a_id_to_cluster_id:
                continue
            self.assertFalse(any([a_id_to_cluster_id.get(d, '') == a_id_to_cluster_id[a_id] for d in dups]))

    def test_remove_dups_not_of_duplicate_type(self):
        artifact_map, cluster_to_contents, duplicate_map, artifact_df = self.get_duplicate_information()
        same_cluster_dups = DuplicateDetector.identify_duplicates_from_same_cluster(duplicate_map, cluster_to_contents, artifact_df)

        intra_cluster_dups, _ = DuplicateDetector._remove_dups_not_of_duplicate_type(set(artifact_map.keys()), duplicate_map,
                                                                                     DuplicateType.INTRA_CLUSTER, artifact_df,
                                                                                     original_clusters_to_contents=cluster_to_contents)
        a_id_to_cluster_id = DictUtil.flip(same_cluster_dups)
        for a_id, dups in intra_cluster_dups.items():
            self.assertTrue(all([a_id_to_cluster_id[d] == a_id_to_cluster_id[a_id] for d in dups]))

        inter_cluster_dups, _ = DuplicateDetector._remove_dups_not_of_duplicate_type(set(artifact_map.keys()), duplicate_map,
                                                                                     DuplicateType.INTER_CLUSTER, artifact_df,
                                                                                     original_clusters_to_contents=cluster_to_contents)
        for a_id, dups in inter_cluster_dups.items():
            if a_id not in a_id_to_cluster_id:
                continue
            self.assertFalse(any([a_id_to_cluster_id.get(d, '') == a_id_to_cluster_id[a_id] for d in dups]))

    def test_find_most_duplicated(self):
        sim_matrix = [[1, 0.9, 0.7, 0.8], [0.9, 1, 0.8, 0.3], [0.8, 0.8, 1, 0.2], [0.8, 0.3, 0.2, 1]]
        duplicate_indices = [(0, 1), (0, 3), (1, 2)]
        count_map, _ = DuplicateDetector.count_duplicates([str(i) for i in range(len(sim_matrix))], duplicate_indices,
                                                          sim_matrix)
        expected_order = [str(i) for i in range(len(sim_matrix))]
        most_to_least = [item[0] for item in sorted(count_map.items(), key=lambda item: item[1], reverse=True)]
        self.assertEqual(expected_order, most_to_least)

        n_times_duplicated = [2, 2, 1, 1]
        for i, n in enumerate(n_times_duplicated):
            self.assertEqual(math.floor(count_map[str(i)]), n)

        duplicate_map = {}
        for i, j in duplicate_indices:
            DictUtil.set_or_append_item(duplicate_map, str(i), str(j), set)
            DictUtil.set_or_append_item(duplicate_map, str(j), str(i), set)

        duplicate_ids = DuplicateDetector.find_most_duplicated_artifacts(count_map, duplicate_map)
        for i, j in duplicate_indices:
            self.assertTrue(str(i) in duplicate_ids)

    def get_duplicate_information(self):
        n_artifacts_per_cluster = 4
        n_clusters = 2
        artifact_map = {string.ascii_lowercase[j * n_artifacts_per_cluster + i]: f"content_{j * n_artifacts_per_cluster + i}"
                        for i in range(n_artifacts_per_cluster) for j in range(n_clusters)}
        cluster_to_contents = {str(j): {a_id for i, a_id in enumerate(artifact_map.values())
                                        if j * n_artifacts_per_cluster <= i < j * n_artifacts_per_cluster + n_artifacts_per_cluster}
                               for j in range(n_clusters)}
        contents = list([list(v) for v in cluster_to_contents.values()])
        duplicate_clusters_contents = {"dup1": {contents[0][0], contents[1][0]},  # intra
                                       "dup2": {contents[0][1], contents[0][2]},  # inter
                                       "dup3": {contents[0][3], contents[1][1], contents[1][2]}}  # mixed
        duplicate_clusters_id = {k: {DictUtil.flip(artifact_map).get(c) for c in v} for k, v in duplicate_clusters_contents.items()}
        duplicate_map = {}
        for cluster in duplicate_clusters_id.values():
            for a_id1 in cluster:
                for a_id2 in cluster:
                    if a_id1 != a_id2:
                        DictUtil.set_or_append_item(duplicate_map, a_id1, a_id2, set)
        artifact_df = ArtifactDataFrame({ArtifactKeys.ID: artifact_map.keys(), ArtifactKeys.CONTENT: artifact_map.values(),
                                         ArtifactKeys.LAYER_ID: ["layer" for _ in artifact_map]})
        return artifact_map, cluster_to_contents, duplicate_map, artifact_df
