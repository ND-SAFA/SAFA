from typing import List

from tgen.clustering.base.cluster_type import ClusterMapType
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.common.objects.artifact import Artifact
from tgen.common.objects.trace import Trace
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep

CLUSTER_ARTIFACT_TYPE = "Cluster"


class ExportClusters(AbstractPipelineStep[ClusteringArgs, ClusteringState]):
    def _run(self, args: ClusteringArgs, state: ClusteringState) -> None:
        cluster_map = state.final_cluster_map

        artifact_df = args.dataset.artifact_df

    @staticmethod
    def create_artifacts_for_clusters(cluster_map: ClusterMapType, artifact_type: str) -> List[Artifact]:
        cluster_ids = cluster_map.keys()
        artifact_id_prefix = artifact_type[0].upper()
        cluster_artifacts = [Artifact(id=ExportClusters.get_cluster_id(cluster_id), content="", layer_id=artifact_type)
                             for cluster_id in cluster_ids]
        return cluster_artifacts

    @staticmethod
    def create_traces_for_clusters(cluster_map: ClusterMapType) -> List[Trace]:
        global_trace_links = []
        for c_id, artifact_ids in cluster_map.items():
            cluster_artifact_id = ExportClusters.get_cluster_id(c_id)
            trace_links = [Trace(source=a_id, target=cluster_artifact_id, score=1, label=1, explanation="") for a_id in artifact_ids]
            global_trace_links = global_trace_links + trace_links
        return global_trace_links

    @staticmethod
    def get_cluster_id(c_id: str):
        return f"{CLUSTER_ARTIFACT_TYPE}{c_id}"
