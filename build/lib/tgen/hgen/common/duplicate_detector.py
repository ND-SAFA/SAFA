from enum import Enum
from typing import Dict, List, Set, Tuple

import numpy as np
from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.keys.structure_keys import ArtifactKeys
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.tools.constants.symbol_constants import DASH
from common_resources.tools.util.dict_util import DictUtil
from common_resources.tools.util.np_util import NpUtil
from common_resources.traceability.relationship_manager.embeddings_manager import EmbeddingsManager

from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.cluster_type import ClusterMapType
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.clustering_pipeline import ClusteringPipeline
from tgen.common.constants.hgen_constants import DEFAULT_DUPLICATE_CLUSTER_MIN_SIM_THRESHOLD, \
    DEFAULT_DUPLICATE_SIMILARITY_THRESHOLD
from tgen.common.util.pipeline_util import nested_pipeline
from tgen.hgen.common.hgen_types import ArtifactPair, CountMap, MatrixIndex
from tgen.hgen.hgen_state import HGenState


class DuplicateType(Enum):
    INTRA_CLUSTER = 0  # duplicates in the same cluster
    INTER_CLUSTER = 1  # duplicates across clusters
    ALL = 2


class DuplicateDetector:
    DUPLICATE_CLUSTER_PREFIX = "r"

    def __init__(self, embeddings_manager: EmbeddingsManager,
                 duplicate_similarity_threshold: float = DEFAULT_DUPLICATE_SIMILARITY_THRESHOLD,
                 duplicate_cluster_min_sim_threshold: float = DEFAULT_DUPLICATE_CLUSTER_MIN_SIM_THRESHOLD,
                 duplicate_sim_sigma: float = None):
        """
        Initializes detector with access to embeddings from manager.
        :param embeddings_manager: Contains the embeddings for the artifacts to be compared.
        :param duplicate_similarity_threshold: The similarity quantile for when two artifacts are too similar.
        :param duplicate_cluster_min_sim_threshold: The cohesion threshold below which a cluster of duplicates will not be accepted.
        :param duplicate_sim_sigma: The number of standard deviations from the mean to flag overly similar artifacts as dups.
        """
        self.embeddings_manager = embeddings_manager
        self.duplicate_similarity_threshold = duplicate_similarity_threshold
        self.duplicate_cluster_min_sim_threshold = duplicate_cluster_min_sim_threshold
        self.duplicate_sim_sigma = duplicate_sim_sigma

    def get_duplicates(self, artifact_df: ArtifactDataFrame,
                       duplicate_type: DuplicateType = DuplicateType.ALL,
                       original_clusters_to_contents: Dict[str, List[str]] = None) -> Tuple[Set[str], Dict[str, Set[str]]]:
        """
        Returns the list of duplicate artifact ids and the list of unique artifact ids.
        :param artifact_df: Contains the artifacts to compare.
        :param duplicate_type: The type of duplicate to search for (between clusters, within clusters or all).
        :param original_clusters_to_contents: Maps the original cluster to a list of each of the artifacts content in that cluster.
        :return: List of duplicate artifact ids and all identified duplicate pairs.
        """
        artifact_ids = list(artifact_df.index)
        if len(artifact_ids) <= 1:
            return set(), {}
        self.embeddings_manager.update_or_add_contents(artifact_df.to_map())
        similarity_matrix = self.embeddings_manager.compare_artifacts(artifact_ids, artifact_ids, include_ids=True)
        duplicate_similarity_threshold = self.calculate_duplicate_similarity_threshold(similarity_matrix)
        similar_indices = NpUtil.get_indices_above_threshold(similarity_matrix, duplicate_similarity_threshold)
        dup_counter, dup_pairs = DuplicateDetector.count_duplicates(artifact_ids, similar_indices, similarity_matrix)
        dup_map = self.create_duplicate_map(dup_pairs)
        duplicate_artifact_ids = set(dup_map.keys())  # self.find_most_duplicated_artifacts(dup_counter, dup_map)
        if duplicate_type != DuplicateType.ALL:
            dup_map, duplicate_artifact_ids = self._remove_dups_not_of_duplicate_type(duplicate_artifact_ids, dup_map, duplicate_type,
                                                                                      artifact_df, original_clusters_to_contents)

        return duplicate_artifact_ids, dup_map

    @nested_pipeline(HGenState)
    def cluster_duplicates(self, artifact_df: ArtifactDataFrame, duplicate_type: DuplicateType = DuplicateType.ALL,
                           original_clusters_to_contents: Dict[str, List[str]] = None,
                           export_path: str = None) -> ClusterMapType:
        """
        Creates clusters of closely related (duplicated) artifacts.
        :param original_clusters_to_contents: Maps the original cluster to a list of each of the artifacts content in that cluster.
        :param artifact_df: Contains all the artifacts that duplicates are being identified for.
        :param duplicate_type: The type of duplicate to search for (between clusters, within clusters or all).
        :param export_path: Path to save clustering output to.
        :return: Dictionary mapping cluster id to the cluster containing duplicates.
        """
        generated_artifact_dataset = PromptDataset(artifact_df=artifact_df)
        cluster_args = ClusteringArgs(dataset=generated_artifact_dataset,
                                      export_dir=export_path,
                                      cluster_max_size=5,
                                      create_dataset=True, allow_duplicates_between_clusters=False,
                                      add_orphans_to_homes=False, allow_singleton_clusters=False,
                                      embedding_manager=self.embeddings_manager)

        clustering_pipeline = ClusteringPipeline(cluster_args)
        clustering_pipeline.run()
        clustering_state = clustering_pipeline.state
        self.embeddings_manager.merge(clustering_state.embedding_manager)

        # ensure matches saved state
        artifacts_df = clustering_state.cluster_dataset.artifact_df.filter_by_row(
            lambda row: row[ArtifactKeys.LAYER_ID.value] != cluster_args.cluster_artifact_type)
        assert len(artifact_df) == len(artifacts_df), "Possibly reloading outdated clustering state."
        artifact_df.index = artifacts_df.index
        artifact_df[ArtifactKeys.CONTENT] = artifacts_df[ArtifactKeys.CONTENT]

        final_cluster_map: ClusterMapType = {}
        for c_id, cluster in clustering_state.final_cluster_map.items():
            duplicate_map = {a_id: cluster.artifact_id_set for a_id in cluster.artifact_id_set}
            dups_from_same_cluster = self.identify_duplicates_from_same_cluster(duplicate_map, original_clusters_to_contents,
                                                                                artifact_df)
            if duplicate_type == DuplicateType.ALL:
                if self._should_add_duplicate_cluster(cluster):
                    if dups_from_same_cluster:
                        originating_clusters = [Cluster.from_artifacts(a_ids, self.embeddings_manager,
                                                                       c_id=DuplicateType.INTRA_CLUSTER.name)
                                                for a_ids in dups_from_same_cluster.values()]
                        _, inter_cluster_artifacts = self._identify_dups_from_inter_clusters(cluster, dups_from_same_cluster)
                        if inter_cluster_artifacts:
                            originating_clusters.append(Cluster.from_artifacts(list(inter_cluster_artifacts), self.embeddings_manager,
                                                                               c_id=DuplicateType.INTER_CLUSTER.name))
                        cluster = Cluster.from_many_clusters(originating_clusters)
                    final_cluster_map[DuplicateDetector.rename_clusters(c_id, duplicate_type)] = cluster
                    continue

            if duplicate_type == DuplicateType.INTRA_CLUSTER:
                self._add_intra_cluster_duplicates(cluster, dups_from_same_cluster, final_cluster_map)
            elif duplicate_type == DuplicateType.INTER_CLUSTER:
                self._add_inter_cluster_duplicates(c_id, cluster, dups_from_same_cluster, final_cluster_map)
        return final_cluster_map

    @staticmethod
    def identify_duplicates_from_same_cluster(duplicate_map: Dict[str, Set[str]], cluster_to_contents: Dict[str, List],
                                              artifact_df: ArtifactDataFrame) -> Dict[str, set]:
        """
        Removes duplicates that originated from the same cluster because less likely to be real duplicates (just related).
        :param duplicate_map: The map of identified duplicate families.
        :param cluster_to_contents: Maps the original cluster to a list of each of the artifacts content in that cluster.
        :param artifact_df: Contains all the artifacts that duplicates are being identified for.
        :return: List of sets of duplicates that came from the same cluster.
        """
        content2cluster = DictUtil.flip(cluster_to_contents)
        same_cluster_duplicate_map = {}
        for a_id, duplicates in duplicate_map.items():
            content = artifact_df.get_artifact(a_id)[ArtifactKeys.CONTENT]
            cluster = content2cluster[content]
            for dup_id in duplicates:
                if dup_id == a_id:
                    continue
                dup_content = artifact_df.get_artifact(dup_id)[ArtifactKeys.CONTENT]
                if content2cluster[dup_content] == cluster:
                    DictUtil.set_or_append_item(same_cluster_duplicate_map, cluster, {dup_id, a_id}, set)

        return same_cluster_duplicate_map

    @staticmethod
    def rename_clusters(orig_cluster_id: str, duplicate_type: DuplicateType) -> str:
        """
        Renames the cluster based on the duplicate type identified from it.
        :param orig_cluster_id: The id originally assigned to the cluster.
        :param duplicate_type: The type of duplicate identified.
        :return: The new name for the cluster.
        """
        return f"{DuplicateDetector.DUPLICATE_CLUSTER_PREFIX}-{orig_cluster_id}-{duplicate_type.value}"

    @staticmethod
    def identify_original_cluster(duplicate_cluster_id: str) -> str:
        """
        Identifies the original cluster based on the name.
        :param duplicate_cluster_id: The id assigned to the duplicate cluster.
        :return: The new name for the cluster.
        """
        name_components = duplicate_cluster_id.split(DASH)
        assert len(name_components) == 3 and name_components[0] == DuplicateDetector.DUPLICATE_CLUSTER_PREFIX \
               and name_components[-1] == str(DuplicateType.INTRA_CLUSTER.value), "Can only identify original cluster " \
                                                                                  "for intra duplicate clusters."
        return name_components[1]

    def calculate_duplicate_similarity_threshold(self, similarity_matrix: np.array) -> float:
        """
        Calculates the duplicate similarity threshold based on the number of artifacts present.
        :param similarity_matrix: The similarity matrix between artifacts being processed.
        :return: The threshold of whether to consider two artifacts as duplicates.
        """
        has_single_score = similarity_matrix.shape[0] <= 2 and similarity_matrix.shape[1] <= 2
        duplicate_similarity_threshold = self.duplicate_similarity_threshold
        if not has_single_score:  # do not use percentile is only single unique
            _, outlier_threshold = NpUtil.get_similarity_matrix_outliers(similarity_matrix, sigma=self.duplicate_sim_sigma)
            duplicate_similarity_threshold = max(duplicate_similarity_threshold, outlier_threshold)
        return duplicate_similarity_threshold

    @staticmethod
    def find_most_duplicated_artifacts(dup_counter: CountMap, dup_map: Dict[str, Set[str]]) -> Set[str]:
        """
        Finds the most duplicated artifacts from the counter.
        :param dup_counter: Contains the number of duplicates each artifact was flagged.
        :param dup_map: Map of duplicate artifact name to a set of all artifact it is duplicated with
        :return: List of most duplicated artifacts.
        """
        most_to_least_overlapping_dups = [d[0] for d in sorted(dup_counter.items(), key=lambda x: x[1], reverse=True)]
        duplicate_artifact_ids: Set[str] = set()
        for dup_art in most_to_least_overlapping_dups:
            if dup_art not in dup_map:
                continue
            if len(dup_map[dup_art].difference(duplicate_artifact_ids)) == 0:
                continue
            can_remove = DuplicateDetector._can_be_removed(dup_art, duplicate_artifact_ids, dup_map)
            if can_remove:
                duplicate_artifact_ids.add(dup_art)
        return duplicate_artifact_ids

    @classmethod
    def count_duplicates(cls, artifact_ids: List[str], duplicate_indices: List[MatrixIndex],
                         similarity_matrix: np.ndarray) -> Tuple[CountMap, Set[ArtifactPair]]:
        """
        Counts the duplicate artifacts and stores the duplicate artifact id pairs.
        :param artifact_ids: The artifact ids referenced by indices.
        :param duplicate_indices: Indices of duplicated artifacts.
        :param similarity_matrix: Contains the similarity comparisons for each artifact pair.
        :return: Map of artifact to duplicate counts and pairs of duplicated artifact ids.
        """
        dup_pairs = set()
        dup_counter: CountMap = {}
        for source_index, target_index in duplicate_indices:
            source_artifact_id = artifact_ids[source_index]
            target_artifact_id = artifact_ids[target_index]

            DictUtil.set_or_increment_count(dup_counter, source_artifact_id)
            DictUtil.set_or_increment_count(dup_counter, target_artifact_id)

            dup_pairs.add((source_artifact_id, target_artifact_id, similarity_matrix[source_index][target_index]))
        avg_similarity = [sum(similarity_matrix[i]) / len(similarity_matrix) for i in range(len(similarity_matrix))]
        for a_id, avg_sim in zip(artifact_ids, avg_similarity):
            if a_id in dup_counter:
                dup_counter[a_id] += avg_sim
        return dup_counter, dup_pairs

    @staticmethod
    def create_duplicate_map(duplicate_pairs: Set[Tuple]) -> Dict:
        """
        Creates a map of an artifact id to a set of its potential dups
        :param duplicate_pairs: A list of tuples containing pairs of artifacts flagged as dups
        :return: A map of an artifact id to a set of its potential dups
        """
        duplicate_map = {}
        for (a1, a2, score) in duplicate_pairs:
            DictUtil.set_or_append_item(duplicate_map, a1, a2, iterable_type=set)
            DictUtil.set_or_append_item(duplicate_map, a2, a1, iterable_type=set)
        return duplicate_map

    def _add_inter_cluster_duplicates(self, c_id: str, cluster: Cluster, dups_from_same_cluster: Dict,
                                      final_cluster_map: ClusterMapType) -> None:
        """
        Adds clusters of duplicates that contain artifacts between the original clusters.
        :param c_id: THe id of dup cluster.
        :param cluster: The cluster of duplicates.
        :param dups_from_same_cluster: Dictionary mapping original cluster_id to the duplicates that came from that cluster.
        :param final_cluster_map: The cluster map to add acceptable clusters of inter-cluster duplicates.
        :return: None
        """
        all_dups_from_same_cluster, inter_cluster_dups = self._identify_dups_from_inter_clusters(cluster, dups_from_same_cluster)
        if inter_cluster_dups:
            base_cluster = Cluster.from_artifacts(inter_cluster_dups, cluster.embedding_manager)
            selected_artifacts = base_cluster.artifact_ids
        elif len(all_dups_from_same_cluster):
            base_cluster = cluster
            selected_artifacts = []
        else:  # all dups are from the same cluster (so not inter cluster)
            return

        for dup_set in dups_from_same_cluster.values():
            best_match = sorted(dup_set, key=lambda dup: base_cluster.similarity_to_neighbors(dup), reverse=True)[0]
            selected_artifacts.append(best_match)

        new_cluster = Cluster.from_artifacts(selected_artifacts, cluster.embedding_manager)
        if self._should_add_duplicate_cluster(new_cluster):
            final_cluster_map[self.rename_clusters(c_id, DuplicateType.INTER_CLUSTER)] = new_cluster

    @staticmethod
    def _identify_dups_from_inter_clusters(duplicate_cluster: Cluster, dups_from_same_cluster: Dict[str, Set[str]]) -> Tuple[Set, Set]:
        """
        Identifies any duplicates that came from different clusters.
        :param duplicate_cluster: The cluster of duplciates.
        :param dups_from_same_cluster: Dictionary mapping OG cluster to the duplicates that came form it.
        :return: A set of dups from the same cluser and a set of dups from different clusters.
        """
        all_dups_from_same_cluster = {d for dups in dups_from_same_cluster.values() for d in dups}
        inter_cluster_dups = duplicate_cluster.artifact_id_set.difference(all_dups_from_same_cluster)
        return all_dups_from_same_cluster, inter_cluster_dups

    def _add_intra_cluster_duplicates(self, cluster: Cluster, dups_from_same_cluster: Dict,
                                      final_cluster_map: ClusterMapType) -> None:
        """
        Adds clusters of duplicates that contain artifacts within the same original cluster.
        :param cluster: The cluster of duplicates.
        :param dups_from_same_cluster: Dictionary mapping original cluster_id to the duplicates that came from that cluster.
        :param final_cluster_map: The cluster map to add acceptable clusters of intra-cluster duplicates.
        :return: None
        """
        for orig_c_id, dups_set in dups_from_same_cluster.items():
            new_cluster = Cluster.from_artifacts(list(dups_set), cluster.embedding_manager)
            if self._should_add_duplicate_cluster(new_cluster):
                new_c_id = self.rename_clusters(orig_c_id, DuplicateType.INTRA_CLUSTER)
                if new_c_id in final_cluster_map:
                    new_cluster.combine_with_cluster(final_cluster_map[new_c_id])
                final_cluster_map[new_c_id] = new_cluster

    def _should_add_duplicate_cluster(self, cluster: Cluster) -> bool:
        """
        Returns True if the duplicate cluster is sufficiently cohesive, otherwise False.
        :param cluster: The cluster to determine if it should be added.
        :return: True if the duplicate cluster is sufficiently cohesive, otherwise False.
        """
        return cluster.min_sim and cluster.min_sim >= self.duplicate_cluster_min_sim_threshold

    @staticmethod
    def _remove_dups_not_of_duplicate_type(duplicate_artifact_ids: Set[str], duplicate_map: Dict[str, Set[str]],
                                           duplicate_type: DuplicateType, artifact_df: ArtifactDataFrame,
                                           original_clusters_to_contents: Dict[str, List[str]]) -> Tuple[Dict, Set]:
        """
        Removes all duplicates that came from the same original cluster.
        :param duplicate_artifact_ids: List of identified duplicate ids.
        :param duplicate_map: Maps identified duplicate id to the set of its duplicates.
        :param duplicate_type: The type of duplicate to search for (between clusters, within clusters or all).
        :param artifact_df: Contains the artifacts to compare.
        :param original_clusters_to_contents: Maps the original cluster to a list of each of the artifacts content in that cluster.
        :return: List of duplicate artifact ids and all identified duplicate pairs.
        :return: The duplicate map and duplicate artifact ids of the specified duplicate type.
        """
        assert original_clusters_to_contents, "Must provide original clusters to select duplicates of specific type"
        dups_from_same_cluster = DuplicateDetector.identify_duplicates_from_same_cluster(duplicate_map,
                                                                                         original_clusters_to_contents,
                                                                                         artifact_df).values()
        refined_duplicate_map = {} if duplicate_type == DuplicateType.INTRA_CLUSTER else duplicate_map
        for dup_set in dups_from_same_cluster:
            for dup in dup_set:
                if duplicate_type == DuplicateType.INTER_CLUSTER:
                    refined_duplicate_map[dup] = refined_duplicate_map[dup].difference(dup_set)
                    if not refined_duplicate_map[dup] and dup in duplicate_artifact_ids:
                        duplicate_artifact_ids.remove(dup)
                else:
                    refined_duplicate_map[dup] = {d for d in dup_set if d != dup}
        if duplicate_type == DuplicateType.INTRA_CLUSTER:
            duplicate_artifact_ids = duplicate_artifact_ids.intersection(refined_duplicate_map.keys())
        return refined_duplicate_map, duplicate_artifact_ids

    @staticmethod
    def _can_be_removed(dup_art: str, removed_duplicate_artifact_ids: Set[str], duplicate_map: Dict[str, Set[str]]) -> bool:
        """
        Determines whether the duplicate can be removed without eliminating its whole cluster
        :param dup_art: The duplicate artifact under consideration
        :param removed_duplicate_artifact_ids: Duplicates that were already removed
        :param duplicate_map: Maps duplicate id to all artifacts it was duplicated with
        :return: True if the duplicate can be removed else False
        """
        already_removed = duplicate_map[dup_art].intersection(removed_duplicate_artifact_ids)
        for other_dup in already_removed:
            if len(duplicate_map[other_dup].difference(removed_duplicate_artifact_ids)) == 1:
                # removing the dup_art will eliminate this whole group
                return False
        return True

    def _add_dups_for_clusters(self, a_id: str, artifact_ids: Set[str], duplicate_map: Dict[str, Set[str]], done: Set[str]) -> bool:
        """
        Adds duplicates to the artifact ids for a particular cluster of duplicates.
        :param a_id: The starting duplicate id.
        :param artifact_ids: List of current artifact ids for the duplicate cluster.
        :param duplicate_map: Mapping of artifact id to its duplicates.
        :param done: Set of duplicates already added to cluster.
        :return: None (updates artifact id set).
        """
        if a_id not in duplicate_map:
            return False
        for d_id in duplicate_map[a_id]:
            if d_id in done:
                continue
            added = self._add_dups_for_clusters(d_id, artifact_ids, duplicate_map, done)
            if added:
                artifact_ids.add(d_id)
                done.add(d_id)
        return True
