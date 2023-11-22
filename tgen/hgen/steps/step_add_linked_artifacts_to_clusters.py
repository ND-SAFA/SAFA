from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.steps.link_orphans import LinkOrphans
from tgen.common.util.clustering_util import ClusteringUtil
from tgen.data.keys.structure_keys import ArtifactKeys, TraceKeys
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.pipeline.abstract_pipeline import AbstractPipelineStep


class AddLinkedArtifactsToClustersStep(AbstractPipelineStep[HGenArgs, HGenState]):

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Adds already linked artifacts to the same cluster as their parent.
        :param args: Arguments to hgen pipeline.
        :param state: Current state of the hgen pipeline.
        :return: None
        """
        if args.perform_clustering and args.add_linked_artifacts_to_cluster and state.original_dataset.trace_dataset:
            original_trace_dataset = state.original_dataset.trace_dataset
            cluster2artifacts = ClusteringUtil.replace_ids_with_artifacts(state.id_to_cluster_artifacts,
                                                                          state.source_dataset.artifact_df)
            for cluster_id, cluster_artifacts in cluster2artifacts.items():
                additional_artifacts = []
                for artifact in cluster_artifacts:
                    child_traces = original_trace_dataset.trace_df.filter_by_row(
                        lambda row: row[TraceKeys.parent_label().value] == artifact[ArtifactKeys.ID]
                                    and row[TraceKeys.LABEL.value] == 1)
                    child_artifacts = [original_trace_dataset.artifact_df.get_artifact(trace[TraceKeys.child_label()])
                                       for i, trace in child_traces.itertuples()]

                    additional_artifacts.extend(child_artifacts)
                cluster_artifacts.extend(additional_artifacts)
            children_ids = {trace[TraceKeys.child_label()] for i, trace in original_trace_dataset.trace_df.filter_by_row(
                lambda row: row[TraceKeys.parent_label().value] in state.source_dataset.artifact_df).itertuples()}
            children_map = {a_id: content for a_id, content in state.original_dataset.artifact_df.to_map().items()
                            if a_id in children_ids or a_id in state.source_dataset.artifact_df}
            state.embedding_manager.update_or_add_contents(children_map, create_embedding=True)
            clustering_args = ClusteringArgs(dataset=state.original_dataset)
            clustering_state = ClusteringState(
                final_cluster_map={cluster_id: Cluster.from_artifacts([a[ArtifactKeys.ID] for a in cluster_artifacts],
                                                                      embeddings_manager=state.embedding_manager)
                                   for cluster_id, cluster_artifacts in cluster2artifacts.items()},
                embedding_manager=state.embedding_manager)
            LinkOrphans().run(clustering_args, clustering_state)

            new_clusters = {c_id for c_id, c_artifacts in clustering_state.final_cluster_map.items()
                            if c_id not in cluster2artifacts}
            state.id_to_cluster_artifacts = {c_id: [a_id for a_id in artifact_ids]
                                             for c_id, artifact_ids in clustering_state.final_cluster_map.items()
                                             if c_id not in new_clusters}
