from tgen.clustering.base.cluster_type import ClusterIdType
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame


class ClusteringUtil:
    @staticmethod
    def replace_ids_with_artifacts(cluster_map: ClusterIdType, artifact_df: ArtifactDataFrame):
        """
        Replaces the artifact ids in the cluster map with the artifacts themselves.
        :param cluster_map: Map from cluster ids to artifacts ids.
        :param artifact_df: Artifact data frame containing artifacts referenced by clusters.
        :return: Cluster map with artifacts instead of artifact ids.
        """
        return {cluster_id: [artifact_df.get_artifact(a_id) for a_id in artifact_ids]
                for cluster_id, artifact_ids in cluster_map.items()}
