from typing import List

from tgen.clustering.base.cluster_type import ClusterMapType
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.objects.artifact import Artifact
from tgen.common.objects.trace import Trace
from tgen.data.keys.structure_keys import ArtifactKeys, TraceKeys
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class AddClustersToDataset(AbstractPipelineStep[ClusteringArgs, ClusteringState]):
    CLUSTER_ARTIFACT_TYPE = "Cluster"

    def _run(self, args: ClusteringArgs, state: ClusteringState) -> None:
        """
        Adds clusters to dataset by introducing artifacts for each cluster and links to the existing artifacts.
        :param args: Arguments to the clustering pipeline.
        :param state: State of the clustering pipeline.
        :return: None
        """
        if not args.add_to_dataset:
            return
        cluster_map = state.final_cluster_map

        artifact_df = args.dataset.trace_dataset.artifact_df
        trace_df = args.dataset.trace_dataset.trace_df
        layer_df = args.dataset.trace_dataset.layer_df

        cluster_artifacts = AddClustersToDataset.create_artifacts_for_clusters(cluster_map)
        cluster_traces = AddClustersToDataset.create_traces_for_clusters(cluster_map)

        artifact_df.add_artifacts(cluster_artifacts)
        trace_df.add_links(cluster_traces)

        referenced_artifact_types = AddClustersToDataset.get_referenced_artifact_types(args.dataset.trace_dataset, cluster_traces)
        for r_artifact_type in referenced_artifact_types:
            layer_df.add_layer(r_artifact_type, AddClustersToDataset.CLUSTER_ARTIFACT_TYPE)

    @classmethod
    def get_referenced_artifact_types(cls, trace_dataset: TraceDataset, traces: List[Trace]) -> List[str]:
        """
        Gets all artifacts types referenced in traces.
        :param trace_dataset: The dataset used to find linked artifacts.
        :param traces: The trace links between artifacts whose artifact types are returned.
        :return: List of artifacts types referenced in traces, excluding cluster type.
        """
        layers = set()
        for t in traces:
            source_type = cls.get_artifact_type(trace_dataset, t[TraceKeys.SOURCE])
            target_type = cls.get_artifact_type(trace_dataset, t[TraceKeys.TARGET])
            layers.add(source_type)
            layers.add(target_type)
        layers.discard(cls.CLUSTER_ARTIFACT_TYPE)
        return list(layers)

    @staticmethod
    def get_artifact_type(trace_dataset: TraceDataset, artifact_id: str):
        """
        Returns artifact type of artifact with name.
        :param trace_dataset: Dataset to search artifact in.
        :param artifact_id: ID of artifact.
        :return: The artifact type.
        """
        return trace_dataset.artifact_df.get_artifact(artifact_id)[ArtifactKeys.LAYER_ID]

    @classmethod
    def create_artifacts_for_clusters(cls, cluster_map: ClusterMapType) -> List[Artifact]:
        """
        Creates artifacts for each cluster.
        :param cluster_map: Map of cluster Id to clusters.
        :return: Artifact for each cluster.
        """
        cluster_ids = cluster_map.keys()
        cluster_artifacts = [Artifact(id=cls.get_cluster_id(cluster_id), content=EMPTY_STRING,
                                      layer_id=cls.CLUSTER_ARTIFACT_TYPE)
                             for cluster_id in cluster_ids]
        return cluster_artifacts

    @staticmethod
    def create_traces_for_clusters(cluster_map: ClusterMapType) -> List[Trace]:
        """
        Creates trace links between cluster artifacts and the artifacts in the cluster.
        :param cluster_map: Maps cluster IDs to artifact IDs.
        :return: Trace links between clusters and artifacts.
        """
        global_trace_links = []
        for c_id, artifact_ids in cluster_map.items():
            cluster_artifact_id = AddClustersToDataset.get_cluster_id(c_id)
            trace_links = [Trace(source=a_id, target=cluster_artifact_id, score=1, label=1, explanation=EMPTY_STRING) for a_id in
                           artifact_ids]
            global_trace_links = global_trace_links + trace_links
        return global_trace_links

    @staticmethod
    def get_cluster_id(c_id: str):
        """
        The artifact ID representing cluster.
        :param c_id: The internal cluster id.
        :return: Name of cluster artifact.
        """
        artifact_id_prefix = AddClustersToDataset.CLUSTER_ARTIFACT_TYPE[0].upper()
        return f"{artifact_id_prefix}{c_id}"
