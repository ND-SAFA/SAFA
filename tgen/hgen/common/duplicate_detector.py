from typing import List, Set, Tuple

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
        :param duplicate_similarity_threshold: The similarity threshold for when two artifacts are too similar.
        """
        self.embeddings_manager = embeddings_manager
        self.duplicate_similarity_threshold = duplicate_similarity_threshold

    def get_duplicates(self, artifact_ids: List[str]) -> Tuple[Set[str], Set[Tuple]]:
        """
        Returns the list of duplicate artifact ids and the list of unique artifact ids.
        :param artifact_ids: The artifacts ids to compare.
        :return: List of duplicate artifact ids and all identified duplicate pairs.
        """
        artifact_embeddings = self.embeddings_manager.get_embeddings(artifact_ids)
        similarity_matrix = EmbeddingUtil.calculate_similarities(artifact_embeddings, artifact_embeddings)
        similar_indices = NpUtil.get_indices_above_threshold(similarity_matrix, self.duplicate_similarity_threshold)
        dup_counter, dup_pairs = DuplicateDetector.count_duplicates(artifact_ids, similar_indices)
        duplicate_artifact_ids = self.find_most_duplicated_artifacts(dup_counter, dup_pairs)
        return duplicate_artifact_ids, dup_pairs

    @staticmethod
    def find_most_duplicated_artifacts(dup_counter: CountMap, dup_pairs: Set[ArtifactPair]) -> Set[str]:
        """
        Finds the most duplicated artifacts from the counter.
        :param dup_counter: Contains the number of duplicates each artifact was flagged.
        :param dup_pairs: Set of duplicate artifact id pairs.
        :return: List of most duplicated artifacts.
        """

        most_to_least_overlapping_dups = [d[0] for d in sorted(dup_counter.items(), key=lambda x: x[1], reverse=True)]
        fixed_dups = set()
        duplicate_artifact_ids: Set[str] = set()
        for dup_art in most_to_least_overlapping_dups:
            for dup_pair in dup_pairs:
                if dup_art in dup_pair and dup_pair not in fixed_dups:
                    fixed_dups.add(dup_pair)
                    duplicate_artifact_ids.add(dup_art)
        return duplicate_artifact_ids

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

