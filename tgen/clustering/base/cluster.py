import os
from copy import deepcopy
from os.path import dirname
from typing import Any, Iterable, List, Tuple, Dict

import numpy as np

from tgen.clustering.methods.supported_clustering_methods import SupportedClusteringMethods
from tgen.common.constants.ranking_constants import DEFAULT_EMBEDDING_MODEL
from tgen.common.util.embedding_util import EmbeddingUtil
from tgen.common.util.np_util import NpUtil
from tgen.common.util.reflection_util import ParamScope, ReflectionUtil
from tgen.embeddings.embeddings_manager import EmbeddingsManager


class Cluster:
    """
    Manages a cluster in a dataset.
    """

    def __init__(self, embeddings_manager: EmbeddingsManager):
        """
        Constructs empty cluster referencing embeddings in manager.
        :param embeddings_manager: The container for all embeddings relating to cluster.
        """
        self.embedding_manager = embeddings_manager
        self.artifact_ids = []
        self.artifact_id_set = set()
        self.votes = 1
        self.__init_stats()

    @staticmethod
    def get_cluster_id(method: SupportedClusteringMethods, index: int):
        """
        Creates generic cluster id.
        :param method: The method used to generate the cluster.
        :param index: The index the cluster is stored in the cluster map.
        :return: The cluster id.
        """
        return f"{method.name}{index}"

    @staticmethod
    def from_artifacts(artifact_ids: List[str], embeddings_manager: EmbeddingsManager) -> "Cluster":
        """
        Creates cluster containing given artifact ids.
        :param artifact_ids: The artifacts to include in the cluster.
        :param embeddings_manager: The embeddings manager used to update the stats of the cluster.
        :return: The cluster.
        """
        cluster = Cluster(embeddings_manager)
        cluster.add_artifacts(artifact_ids)
        return cluster

    @staticmethod
    def from_artifact_map(artifact_map: Dict[Any, str], model_name: str = DEFAULT_EMBEDDING_MODEL,
                          update_stats: bool = True) -> "Cluster":
        """
        Creates cluster containing given artifacts in the map.
        :param artifact_map: The  id to content of artifacts to include in the cluster.
        :param model_name: The name of the model to use in the embeddings manager
         :param update_stats: If True, updates the cluster stats.
        :return: The cluster.
        """
        embeddings_manager = EmbeddingsManager(artifact_map, model_name=model_name)
        cluster = Cluster(embeddings_manager)
        cluster.add_artifacts(list(artifact_map.keys()), update_stats=update_stats)
        return cluster

    def add_vote(self) -> None:
        """
        Adds vote to cluster.
        :return: None. Modified in place.
        """
        self.votes += 1

    def add_artifacts(self, artifact_ids: List[str], update_stats: bool = True) -> None:
        """
        Adds multiple artifacts to cluster and updates its stats.
        :param artifact_ids: The artifact ids to add to the cluster.
        :param update_stats: If True, updates the cluster stats.
        :return: None.
        """
        for artifact_id in artifact_ids:
            self._add_artifact(artifact_id)
        if update_stats:
            self.__update_stats()

    def add_artifact(self, artifact_id: str, update_stats: bool = True) -> None:
        """
        Adds an artifact to the cluster.
        :param artifact_id: ID of artifact to add to cluster.
        :param update_stats: If True, updates the cluster stats.
        :return: None.
        """
        self._add_artifact(artifact_id)
        if update_stats:
            self.__update_stats()

    def similarity_to(self, cluster: "Cluster") -> float:
        """
        Calculates the cosine similarity between the centroid of this cluster to the cluster given.
        :param cluster: The cluster to calculate the distance to.
        :return: The similarity to the other cluster.
        """
        return EmbeddingUtil.calculate_similarities([self.centroid], [cluster.centroid])[0][0]

    def similarity_to_neighbors(self, a_id: str) -> float:
        """
        Calculates the average similarity to the cluster's artifacts.
        :param a_id: Artifact id to compare to cluster.
        :return: Average similarity.
        """
        unique_artifacts_embeddings = [self.embedding_manager.get_embedding(a) for a in self.artifact_id_set if a != a_id]
        if len(unique_artifacts_embeddings) == 0:
            return 1
        artifact_embedding = [self.embedding_manager.get_embedding(a_id)]
        similarities = EmbeddingUtil.calculate_similarities(artifact_embedding, unique_artifacts_embeddings)[0]
        avg_sim = sum(similarities) / len(similarities)
        return avg_sim

    def _add_artifact(self, artifact_id: str) -> None:
        """
        Adds an artifact to the cluster.
        :param artifact_id: ID of artifact to add to cluster.
        :return: None
        """
        if artifact_id not in self.artifact_id_set:
            self.artifact_id_set.add(artifact_id)
            self.artifact_ids.append(artifact_id)

    def __update_stats(self) -> None:
        """
        Calculates all statistics for the cluster.
        :return: None, stats are set in place
        """
        self.centroid = self.embedding_manager.calculate_centroid(self.artifact_ids)
        self.avg_similarity = self.__calculate_average_similarity()
        if len(self.artifact_id_set) > 1:
            self.similarity_matrix = self.__calculate_similarity_matrix()
            self.min_sim, self.max_sim = self.__calculate_min_max_similarity()
            self.avg_pairwise_sim = self.__calculate_avg_pairwise_distance()

    def __init_stats(self) -> None:
        """
        Sets all stats back to their initial state
        :return:
        """
        self.avg_similarity = None
        self.centroid = None
        self.similarity_matrix = None
        self.min_sim = None
        self.max_sim = None
        self.avg_pairwise_sim = None

    def __calculate_average_similarity(self) -> float:
        """
        Calculates the average similarity from the artifacts to the centroid.
        :return: Average similarity to centroid.
        """
        artifact_embeddings = [self.embedding_manager.get_embedding(a_id) for a_id in self.artifact_ids]
        similarities = EmbeddingUtil.calculate_similarities([self.centroid], artifact_embeddings)[0]
        return np.sum(similarities) / len(similarities)

    def __calculate_similarity_matrix(self) -> np.array:
        """
        Calculates the similarity scores between all artifacts in the cluster.
        :return: The similarity matrix.
        """
        artifact_embeddings = [self.embedding_manager.get_embedding(a_id) for a_id in self.artifact_ids]
        similarity_matrix = EmbeddingUtil.calculate_similarities(artifact_embeddings, artifact_embeddings)
        return similarity_matrix

    def __calculate_min_max_similarity(self) -> Tuple[float, float]:
        """
        Calculates the minimum and maximum similarity scores in the similarity matrix.
        :return: Min and Max similarity scores.
        """
        unique_indices = NpUtil.get_unique_indices(len(self.artifact_id_set))
        similarities = self.get_values(self.similarity_matrix, unique_indices)
        min_sim = np.min(similarities)
        max_sim = np.max(similarities)
        return min_sim, max_sim

    def __calculate_avg_pairwise_distance(self) -> float:
        """
        Calculates the average pairwise distance between all points of a matrix.
        :return: Calculates the pairwise distances and returns its average.
        """
        n_artifacts = len(self.artifact_id_set)
        indices = NpUtil.get_unique_indices(n_artifacts)
        unique_scores = self.get_values(self.similarity_matrix, indices)
        return sum(unique_scores) / len(unique_scores)

    @staticmethod
    def get_values(matrix: np.array, indices: List[Tuple[int, int]]):
        """
        Gets the values in the matrix. TODO: Replace with actual numpy notation.
        :param matrix: The matrix to index.
        :param indices: The index in the matrix to retrieve. Expected to be 2D.
        :return: List of values in the matrix.
        """
        values = [matrix[i][j] for i, j in indices]
        return values

    def to_yaml(self, export_path: str = None, **kwargs) -> "Cluster":
        """
        Removes stats that take a while to be saved
        :param export_path: Path to save yaml to.
        :return: The cluster cleaned up for efficient saving as yaml
        """
        if export_path:
            yaml_safe_cluster = deepcopy(self)
            yaml_safe_cluster.__init_stats()
            export_path = os.path.join(dirname(export_path), ReflectionUtil.extract_name_of_variable(f"{self.embedding_manager=}",
                                                                                                     is_self_property=True))
            yaml_safe_cluster.embedding_manager = yaml_safe_cluster.embedding_manager.to_yaml(export_path)
            return yaml_safe_cluster
        return self

    def from_yaml(self, **kwargs) -> "Cluster":
        """
        Updates states after loading from yaml
        :return: The Cluster with updated states
        """
        self.__update_stats()
        return self

    def __len__(self) -> int:
        """
        :return: Length of cluster is the number of the artifacts in cluster.
        """
        return len(self.artifact_id_set)

    def __iter__(self) -> Iterable[str]:
        """
        :return: Iterable goes through each artifact id.
        """
        for a in self.artifact_ids:
            yield a

    def __deepcopy__(self, memo):
        """
        Copies the cluster with the minimal properties need to recreate stastics and overall state of current cluster.
        :param memo: Ignored.
        :return: The copy of the cluster.
        """
        c = Cluster(self.embedding_manager)
        keep_props = ["artifact_ids", "artifact_id_set", "votes"]
        ReflectionUtil.copy_attributes(self, c, ParamScope.PRIVATE, fields=keep_props)
        return c

    def __contains__(self, item: Any) -> bool:
        """
        Calculates whether item is an artifact ID in the cluster.
        :param item: The artifact ID.
        :return: True is artifact id in cluster, false otherwise.
        """
        return isinstance(item, str) and item in self.artifact_ids

    def __str__(self) -> str:
        """
        :return: Returns string version of the artifacts.
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        :return: Cluster is represented by the list of artifact ids it contains.
        """
        metrics = {"AVG": self.avg_similarity, "MIN": self.min_sim, "MAX": self.max_sim, "P": self.avg_pairwise_sim}
        metrics = {k: round(v, 2) for k, v in metrics.items() if v is not None}
        cluster_repr = f"{self.artifact_ids.__str__()}{str(metrics)}"
        return cluster_repr

    def __eq__(self, other: Any) -> bool:
        """
        Determines if other contains the same artifacts as this one.
        :param other: The other cluster to compare.
        :return: True if clusters have the same artifacts, false otherwise.
        """
        return isinstance(other, Cluster) and other.artifact_id_set.__eq__(self.artifact_id_set)

    def __hash__(self) -> List[Any]:
        """
        Makes this object hashable.
        # TODO: Replace this with the hash for a set.
        :return: The hash for each artifact id.
        """
        return hash("-".join(sorted(list(self.artifact_ids))))
