from typing import Dict, List, Set, Tuple

from tgen.common.constants.hgen_constants import DUPLICATE_THRESHOLD_PERCENTILE
from tgen.common.util.dict_util import DictUtil
from tgen.common.util.embedding_util import EmbeddingUtil
from tgen.common.util.np_util import NpUtil
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.hgen.common.hgen_types import ArtifactPair, CountMap, MatrixIndex


class DuplicateDetector:
    def __init__(self, embeddings_manager: EmbeddingsManager, duplicate_similarity_threshold: float):
        """
        Initializes detector with access to embeddings from manager.
        :param embeddings_manager: Contains the embeddings for the artifacts to be compared.
        :param duplicate_similarity_threshold: The similarity quantile for when two artifacts are too similar.
        """
        self.embeddings_manager = embeddings_manager
        self.duplicate_similarity_threshold = duplicate_similarity_threshold

    def get_duplicates(self, artifact_ids: List[str]) -> Tuple[Set[str], Dict[str, Set[str]]]:
        """
        Returns the list of duplicate artifact ids and the list of unique artifact ids.
        :param artifact_ids: The artifacts ids to compare.
        :return: List of duplicate artifact ids and all identified duplicate pairs.
        """
        artifact_embeddings = self.embeddings_manager.get_embeddings(artifact_ids)
        similarity_matrix = EmbeddingUtil.calculate_similarities(artifact_embeddings, artifact_embeddings)
        duplicate_similarity_threshold = NpUtil.get_similarity_matrix_percentile(similarity_matrix, DUPLICATE_THRESHOLD_PERCENTILE)
        duplicate_similarity_threshold = max(duplicate_similarity_threshold, self.duplicate_similarity_threshold)
        similar_indices = NpUtil.get_indices_above_threshold(similarity_matrix, duplicate_similarity_threshold)
        dup_counter, dup_pairs = DuplicateDetector.count_duplicates(artifact_ids, similar_indices)
        dup_map = self.create_duplicate_map(dup_pairs)
        duplicate_artifact_ids = self.find_most_duplicated_artifacts(dup_counter, dup_map)
        return duplicate_artifact_ids, dup_map

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
            if len(dup_map[dup_art].difference(duplicate_artifact_ids)) == 0:
                continue
            can_remove = DuplicateDetector._can_be_removed(dup_art, duplicate_artifact_ids, dup_map)
            if can_remove:
                duplicate_artifact_ids.add(dup_art)
        return duplicate_artifact_ids

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

    @classmethod
    def count_duplicates(cls, artifact_ids: List[str], duplicate_indices: List[MatrixIndex]) -> Tuple[CountMap, Set[ArtifactPair]]:
        """
        Counts the duplicate artifacts and stores the duplicate artifact id pairs.
        :param artifact_ids: The artifact ids referenced by indices.
        :param duplicate_indices: Indices of duplicated artifacts.
        :return: Map of artifact to duplicate counts and pairs of duplicated artifact ids.
        """
        dup_pairs = set()
        dup_counter: CountMap = {}
        for source_index, target_index in duplicate_indices:
            source_artifact_id = artifact_ids[source_index]
            target_artifact_id = artifact_ids[target_index]

            DictUtil.set_or_increment_count(dup_counter, source_artifact_id, 1)
            DictUtil.set_or_increment_count(dup_counter, target_artifact_id, 1)

            dup_pairs.add((source_artifact_id, target_artifact_id))
        return dup_counter, dup_pairs

    @staticmethod
    def create_duplicate_map(duplicate_pairs: Set[Tuple]) -> Dict:
        """
        Creates a map of an artifact id to a set of its potential dups
        :param duplicate_pairs: A list of tuples containing pairs of artifacts flagged as dups
        :return: A map of an artifact id to a set of its potential dups
        """
        duplicate_map = {}
        for (a1, a2) in duplicate_pairs:
            DictUtil.set_or_append_item(duplicate_map, a1, a2, iterable_type=set)
            DictUtil.set_or_append_item(duplicate_map, a2, a1, iterable_type=set)
        return duplicate_map
