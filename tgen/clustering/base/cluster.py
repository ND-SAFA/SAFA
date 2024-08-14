import os
import uuid
from copy import deepcopy
from os.path import dirname
from typing import Any, Callable, Dict, Iterable, List, Tuple, Union

import numpy as np
import pandas as pd
from common_resources.tools.constants.environment_constants import DEFAULT_EMBEDDING_MODEL

from tgen.clustering.methods.supported_clustering_methods import SupportedClusteringMethods
from common_resources.tools.util.list_util import ListUtil
from common_resources.tools.util.np_util import NpUtil
from common_resources.tools.util.reflection_util import ParamScope, ReflectionUtil
from tgen.relationship_manager.embeddings_manager import EmbeddingsManager


class Cluster:
    """
    Manages a cluster in a dataset.
    """
    CENTROID_KEY = "centroid"

    def __init__(self, embeddings_manager: EmbeddingsManager, c_id: str = None):
        """
        Constructs empty cluster referencing embeddings in manager.
        :param embeddings_manager: The container for all embeddings relating to cluster.
        :param c_id: The cluster id.
        """
        self.embedding_manager = embeddings_manager
        self.artifact_ids = []
        self.artifact_id_set = set()
        self.votes = 1
        self.id = str(uuid.uuid4()) if not c_id else c_id
        self.__originating_clusters = []
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
    def from_artifacts(artifact_ids: List[str], embeddings_manager: EmbeddingsManager, c_id: str = None) -> "Cluster":
        """
        Creates cluster containing given artifact ids.
        :param artifact_ids: The artifacts to include in the cluster.
        :param embeddings_manager: The embeddings manager used to update the stats of the cluster.
        :param c_id: The cluster id.
        :return: The cluster.
        """
        cluster = Cluster(embeddings_manager, c_id=c_id)
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

    def remove_artifacts(self, artifact_ids: List[str], update_stats: bool = True) -> None:
        """
        Removes multiple artifacts from cluster and updates its stats.
        :param artifact_ids: The artifact ids to remove.
        :param update_stats: If True, updates the cluster stats.
        :return: None.
        """
        self._commit_action(self._remove_artifact, artifact_ids, update_stats)

    def add_artifacts(self, artifact_ids: Union[List[str], str], update_stats: bool = True) -> None:
        """
        Adds multiple artifacts to cluster and updates its stats.
        :param artifact_ids: The artifact ids to add to the cluster.
        :param update_stats: If True, updates the cluster stats.
        :return: None.
        """
        self._commit_action(self._add_artifact, artifact_ids, update_stats)

    def similarity_to(self, cluster: "Cluster") -> float:
        """
        Calculates the cosine similarity between the centroid of this cluster to the cluster given.
        :param cluster: The cluster to calculate the distance to.
        :return: The similarity to the other cluster.
        """
        return self.embedding_manager.compare_artifacts([self.get_centroid_key()], [cluster.get_centroid_key()])[0][0]

    def similarity_to_neighbors(self, a_id: str) -> float:
        """
        Calculates the average similarity to the cluster's artifacts.
        :param a_id: Artifact id to compare to cluster.
        :return: Average similarity.
        """
        unique_artifacts_ids = [a for a in self.artifact_id_set if a != a_id]
        if len(unique_artifacts_ids) == 0:
            return 1
        similarities = self.embedding_manager.compare_artifacts([a_id], unique_artifacts_ids)[0]
        avg_sim = sum(similarities) / len(similarities)
        return avg_sim

    def get_content_of_artifacts_in_cluster(self) -> List[str]:
        """
        Gets the content of all artifacts in the cluster.
        :return: A list of the content of all artifacts in the cluster.
        """
        return [self.embedding_manager.get_content(a_id) for a_id in self.artifact_ids]

    def get_content(self, a_id: str) -> str:
        """
        Gets content for a specific artifact.
        :param a_id: The id of the artifact to get content for.
        :return: The content of the specified artifact.
        """
        return self.embedding_manager.get_content(a_id)

    def to_yaml(self, export_path: str = None, **kwargs) -> "Cluster":
        """
        Removes stats that take a while to be saved
        :param export_path: Path to save yaml to.
        :return: The cluster cleaned up for efficient saving as yaml
        """
        if export_path:
            yaml_safe_cluster = deepcopy(self)
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

    def calculate_avg_pairwise_sim_for_artifacts(self, artifact_ids: Union[List[str], str]) -> Union[float, List[float]]:
        """
        Calculates the avg pairwise similarity of an artifact to its neighbors.
        :param artifact_ids: The id(s) of the artifact(s) to calculate the avg pairwise sim of.
        :return: The avg pairwise similarity of each artifact to its neighbors.
        """
        if isinstance(artifact_ids, list):
            return [self.calculate_avg_pairwise_sim_for_artifact(a_id) for a_id in artifact_ids]
        else:
            return self.calculate_avg_pairwise_sim_for_artifact(artifact_ids)

    def calculate_avg_pairwise_sim_for_artifact(self, artifact_id: str) -> float:
        """
        Calculates the avg pairwise similarity of an artifact to its neighbors.
        :param artifact_id: The id of the artifact to calculate the avg pairwise sim of.
        :return: The avg pairwise similarity of an artifact to its neighbors.
        """
        artifact_index = self.artifact_ids.index(artifact_id)
        neighbor_indices = [i for i in range(self.similarity_matrix.shape[1]) if i != artifact_index]
        neighbor_similarities = self.similarity_matrix[artifact_index, neighbor_indices]
        return sum(neighbor_similarities) / len(neighbor_similarities)

    def combine_with_cluster(self, other_cluster: "Cluster") -> None:
        """
        Merges another cluster in with this one.
        :param other_cluster: Cluster to merge in.
        :return: A cluster that is a combination of the original and other cluster.
        """
        if not self.__originating_clusters:
            current_cluster = Cluster.from_artifacts(self.artifact_ids, self.embedding_manager, c_id=self.id)
            self.__originating_clusters.append(current_cluster)
        self.embedding_manager.merge(other_cluster.embedding_manager)
        self.add_artifacts(other_cluster.artifact_ids, update_stats=True)
        self.__originating_clusters.append(other_cluster)

    @staticmethod
    def from_many_clusters(originating_clusters: List["Cluster"]) -> "Cluster":
        """
        Creates a cluster from many smaller ones.
        :param originating_clusters: The clusters to combine to create a new cluster.
        :return: A cluster that results from the combination of all the smalelr ones.
        """
        cluster = originating_clusters[0]
        if len(originating_clusters) > 1:
            for c in originating_clusters[1:]:
                cluster.combine_with_cluster(c)
        else:
            cluster.__originating_clusters = originating_clusters
        return cluster

    def get_originating_clusters(self) -> List["Cluster"]:
        """
        If the cluster originated from the combination of multiple clusters, then returns a list of all original clusters.
        :return: List of all original clusters from which the current one came.
        """
        return self.__originating_clusters

    def remove_outliers(self, sim_sigma: float = 1.5, min_std: float = 0.05, eps: float = 0.005) -> bool:
        """
        Removes any artifacts that are much different than the rest.
        :param sim_sigma: The number of stds from the mean to consider an outlier.
        :param min_std: If a cluster has less std between artifacts than the min, no outliers will be removed.
        :param eps: Slight offset from the outlier threshold.
        :return: True if removed an outlier else False.
        """
        scores = [self.similarity_to_neighbors(a) for a in self.artifact_ids]
        scores_std = pd.Series(scores).std()
        if scores_std >= min_std:
            sorted_artifact_scores = ListUtil.zip_sort(self.artifact_ids, scores)
            sorted_artifacts, sorted_scores = ListUtil.unzip(sorted_artifact_scores)
            lower, upper = NpUtil.detect_outlier_scores(scores, sigma=sim_sigma)
            outliers = [a for a, score in sorted_artifact_scores if score < lower + eps]
            if outliers:
                self._remove_artifact(sorted_artifacts[0])
                return True
        return False

    @staticmethod
    def weight_average_pairwise_sim_with_size(avg_pairwise_sim: float, size: int, size_weight: float = 0.15) -> float:
        """
        Calculates the average pairwise distance between all points of a matrix, weighted with the size of the cluster.
        :param avg_pairwise_sim: The average pairwise distance.
        :param size: The size of the cluster.
        :param size_weight: The amount by which the log of the size should be weighted with the avg. pairwise sim.
        :return: Calculates the pairwise distances and returns its average, weighted with the size of the cluster.
        """
        return (size_weight * np.log(size)) + avg_pairwise_sim

    def calculate_importance(self, primary_metric: str):
        """
        Calculates how important the cluster is compared to other candidates.
        :param primary_metric: The primary metric to consider.
        :return: The importance of the cluster.
        """
        primary_metric = getattr(self, primary_metric)
        if not primary_metric:
            return 0
        return primary_metric * self.votes

    def get_centroid_key(self) -> str:
        """
        Creates a key representing the centroid of this cluster.
        :return: The centroid key.
        """
        return f"{self.CENTROID_KEY}{self.id}"

    def _commit_action(self, action: Callable, artifact_ids: Union[List[str], str], update_stats: bool) -> None:
        """
        Performs an action on all given artifacts.
        :param action: The method used to perform the action.
        :param artifact_ids: The ids of the artifacts to perform action for.
        :param update_stats: If True, updates the clusters stats.
        :return: None.
        """
        if isinstance(artifact_ids, str):
            artifact_ids = [artifact_ids]
        for artifact_id in artifact_ids:
            action(artifact_id)
        if update_stats:
            self.__update_stats()

    def _add_artifact(self, artifact_id: str) -> None:
        """
        Adds an artifact to the cluster.
        :param artifact_id: ID of artifact to add to cluster.
        :return: None
        """
        if artifact_id not in self.artifact_id_set:
            self.artifact_id_set.add(artifact_id)
            self.artifact_ids.append(artifact_id)

    def _remove_artifact(self, artifact_id: str) -> None:
        """
        Adds an artifact to the cluster.
        :param artifact_id: ID of artifact to add to cluster.
        :return: None
        """
        if artifact_id in self.artifact_id_set:
            self.artifact_id_set.remove(artifact_id)
            self.artifact_ids.remove(artifact_id)

    def __update_stats(self) -> None:
        """
        Calculates all statistics for the cluster.
        :return: None, stats are set in place
        """
        self.centroid = self.embedding_manager.calculate_centroid(self.artifact_ids, key_to_add_to_map=self.get_centroid_key())
        self.avg_similarity = self.__calculate_average_similarity()
        if len(self.artifact_id_set) > 1:
            self.similarity_matrix = self.__calculate_similarity_matrix()
            self.min_sim, self.max_sim, self.med_sim = self.__calculate_min_max_median_similarity()
            self.avg_pairwise_sim = self.__calculate_avg_pairwise_distance()
            self.size_weighted_sim = self.weight_average_pairwise_sim_with_size(self.avg_pairwise_sim, len(self))

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
        self.size_weighted_sim = None
        self.importance = None

    def __calculate_avg_pairwise_distance(self) -> float:
        """
        Calculates the average pairwise distance between all points of a matrix.
        :return: Calculates the pairwise distances and returns its average.
        """
        n_artifacts = len(self.artifact_id_set)
        indices = NpUtil.get_unique_indices(n_artifacts)
        unique_scores = NpUtil.get_values(self.similarity_matrix, indices)
        unique_scores.append(min(unique_scores))  # increase weight of min
        return sum(unique_scores) / len(unique_scores)

    def __calculate_average_similarity(self) -> float:
        """
        Calculates the average similarity from the artifacts to the centroid.
        :return: Average similarity to centroid.
        """
        similarities = self.embedding_manager.compare_artifacts([self.get_centroid_key()], self.artifact_ids)[0]
        return np.sum(similarities) / len(similarities)

    def __calculate_similarity_matrix(self) -> np.array:
        """
        Calculates the similarity scores between all artifacts in the cluster.
        :return: The similarity matrix.
        """
        similarity_matrix = self.embedding_manager.compare_artifacts(self.artifact_ids)
        return similarity_matrix

    def __calculate_min_max_median_similarity(self) -> Tuple[float, float, float]:
        """
        Calculates the minimum and maximum similarity scores in the similarity matrix.
        :return: Min and Max similarity scores.
        """
        unique_indices = NpUtil.get_unique_indices(len(self.artifact_id_set))
        similarities = NpUtil.get_values(self.similarity_matrix, unique_indices)
        min_sim = np.min(similarities)
        max_sim = np.max(similarities)
        med_sim = np.median(similarities)
        return min_sim, max_sim, med_sim

    def __calculate_importance(self) -> float:
        """
        Calculates the importance of the cluster compared to other candidates.
        :return: The importance score.
        """
        if self.size_weighted_sim:
            return self.size_weighted_sim * self.votes

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
        metrics = {"AVG": self.avg_similarity, "MIN": self.min_sim, "MAX": self.max_sim,
                   "P": self.avg_pairwise_sim, "IMPORTANCE": self.size_weighted_sim}
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

    def __hash__(self) -> int:
        """
        Makes this object hashable.
        :return: The hash for each artifact id.
        """
        return hash("-".join(sorted(list(self.artifact_id_set))))
