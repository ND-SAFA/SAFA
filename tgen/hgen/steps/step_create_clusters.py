from tgen.clustering.base.cluster_type import ClusterMapType
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.clustering_pipeline import ClusteringPipeline
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class CreateClustersStep(AbstractPipelineStep[HGenArgs, HGenState]):
    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Creates clusters from source artifacts to generate new artifacts for each clusters.
        :param args: Arguments to hgen pipeline.
        :param state: Current state of the hgen pipeline.
        :return: None
        """
        args = ClusteringArgs(dataset=state.source_dataset, create_dataset=True)
        clustering_pipeline = ClusteringPipeline(args)
        clustering_pipeline.run()

        cluster_map = clustering_pipeline.state.final_cluster_map
        state.cluster_dataset = clustering_pipeline.state.cluster_dataset
        source_artifact_df = state.source_dataset.artifact_df
        state.id_to_cluster_artifacts = self._replace_ids_with_artifacts(cluster_map, source_artifact_df)

    @staticmethod
    def _replace_ids_with_artifacts(cluster_map: ClusterMapType, artifact_df: ArtifactDataFrame):
        """
        Replaces the artifact ids in the cluster map with the artifacts themselves.
        :param cluster_map: Map from cluster ids to artifacts ids.
        :param artifact_df: Artifact data frame containing artifacts referenced by clusters.
        :return: Cluster map with artifacts instead of artifact ids.
        """
        return {cluster_id: [artifact_df.get_artifact(a_id) for a_id in artifact_ids]
                for cluster_id, artifact_ids in cluster_map.items()}
