from collections import OrderedDict
from typing import Dict, List

from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame

from tgen.clustering.base.cluster_type import ClusterIdType, ClusterMapType


class ClusteringUtil:
    @staticmethod
    def replace_ids_with_artifacts(cluster_map: ClusterIdType, artifact_df: ArtifactDataFrame) -> Dict[str, List]:
        """
        Replaces the artifact ids in the cluster map with the artifacts themselves.
        :param cluster_map: Map from cluster ids to artifacts ids.
        :param artifact_df: Artifact data frame containing artifacts referenced by clusters.
        :return: Cluster map with artifacts instead of artifact ids.
        """
        return OrderedDict({cluster_id: [artifact_df.get_artifact(a_id, throw_exception=True) for a_id in artifact_ids]
                            for cluster_id, artifact_ids in cluster_map.items()})

    @staticmethod
    def convert_cluster_map_to_artifact_format(cluster_map: ClusterMapType, artifact_df: ArtifactDataFrame = None) -> Dict[str, List]:
        """
        Converts the cluster map to cluster id -> artifact ids or if artifact df is provided then cluster id -> artifact dict.
        :param cluster_map: Map from cluster ids to artifacts ids.
        :param artifact_df: Artifact data frame containing artifacts referenced by clusters.
        :return: Cluster map with artifacts or artifact ids.
        """
        converted = {str(k): sorted(v.artifact_ids, key=lambda a_id: v.similarity_to_neighbors(a_id), reverse=True)
                     for k, v in cluster_map.items()}
        if artifact_df is None:
            return converted
        return ClusteringUtil.replace_ids_with_artifacts(converted, artifact_df)
