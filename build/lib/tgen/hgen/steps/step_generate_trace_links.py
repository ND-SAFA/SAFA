from typing import Dict, List, Set, Tuple

from common_resources.data.keys.structure_keys import TraceKeys
from common_resources.tools.constants.model_constants import USE_NL_SUMMARY_EMBEDDINGS

from tgen.common.constants.hgen_constants import RELATED_CHILDREN_SCORE, WEIGHT_OF_PRED_RELATED_CHILDREN
from common_resources.tools.t_logging.logger_manager import logger
from common_resources.data.objects.trace import Trace
from common_resources.tools.util.enum_util import EnumDict
from common_resources.tools.util.file_util import FileUtil
from common_resources.tools.util.math_util import MathUtil
from tgen.hgen.common.hgen_util import HGenUtil
from tgen.hgen.common.special_doc_types import DocTypeConstraints
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.steps.sort_children_step import SortChildrenStep
from tgen.tracing.ranking.trace_selectors.select_by_threshold import SelectByThreshold
from tgen.tracing.ranking.trace_selectors.selection_by_threshold_scaled_across_all import SelectByThresholdScaledAcrossAll
from tgen.tracing.ranking.trace_selectors.selection_by_threshold_scaled_by_artifact import SelectByThresholdScaledByArtifacts


class GenerateTraceLinksStep(AbstractPipelineStep[HGenArgs, HGenState]):

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Generates trace links between the new generated artifacts and the source artifacts
        :param state: The current state of hgen at this point in time
        :param args: The arguments and current state of HGEN.
        :return: None
        """
        logger.info(f"Predicting links between {args.target_type} and {args.source_layer_ids}\n")

        if args.perform_clustering:
            trace_predictions, selected_predictions = self._trace_artifacts_in_cluster_to_generated_parents(args, state)
        else:
            trace_predictions = self._run_tracing_job_on_all_artifacts(args, state)
            trace_predictions = self._weight_scores_with_related_children_predictions(trace_predictions,
                                                                                      state.id_to_related_children)
            selected_predictions = SelectByThresholdScaledByArtifacts.select(trace_predictions, args.link_selection_threshold)
        state.selected_predictions = selected_predictions
        state.trace_predictions = trace_predictions

    def _run_tracing_job_on_all_artifacts(self, args: HGenArgs, state: HGenState) -> List[EnumDict]:
        """
        Runs a ranking job for all candidate links between the children and generated parents
        :param args: The arguments to HGen
        :param state: The current state of HGen
        :return: The trace predictions for all candidates (that were not filtered)
        """
        children_ids = list(state.all_artifacts_dataset.artifact_df.get_artifacts_by_type(args.source_layer_ids).index)
        parent_ids = list(state.all_artifacts_dataset.artifact_df.get_artifacts_by_type(args.target_type).index)

        selected_entries = self._run_embedding_pipeline(args, state, parent_ids=parent_ids, children_ids=children_ids,
                                                        export_dir=HGenUtil.get_ranking_dir(state.export_dir))
        trace_predictions: List[EnumDict] = selected_entries
        return trace_predictions

    def _trace_artifacts_in_cluster_to_generated_parents(self, args: HGenArgs, state: HGenState) -> Tuple[List[Trace], List[Trace]]:
        """
        Generates links between the artifacts in a cluster and the parent artifact generated from the cluster artifacts
        :param args: The arguments to HGen
        :param state: The current state of HGen
        :return: The trace predictions for the clusters
        """
        trace_predictions, trace_selections = [], []
        new_artifact_map = state.all_artifacts_dataset.artifact_df.to_map(use_code_summary_only=not USE_NL_SUMMARY_EMBEDDINGS)

        state.all_artifacts_dataset.project_summary = args.dataset.project_summary
        state.embedding_manager.update_or_add_contents(new_artifact_map)

        generation2id = {content: a_id for a_id, content in new_artifact_map.items()}
        subset_ids = list({a_id for a_ids in state.get_cluster2artifacts(ids_only=True).values() for a_id in a_ids})
        subset_ids += list(state.new_artifact_dataset.artifact_df.index)
        state.embedding_manager.create_embeddings(artifact_ids=subset_ids)
        for cluster_id, generations in state.get_cluster2generation().items():
            parent_ids = [generation2id[generation] for generation in generations if
                          generation in generation2id]  # ignores if dup deleted already
            if len(parent_ids) == 0:
                continue
            self._add_cluster_predictions(args, state, cluster_id, parent_ids, trace_predictions, trace_selections)
        self._trace_orphan_children(state, trace_predictions, trace_selections)
        return trace_predictions, trace_selections

    def _add_cluster_predictions(self, args: HGenArgs, state: HGenState, cluster_id: str, parent_ids: List[str],
                                 trace_predictions: List[Trace], trace_selections: List[Trace]) -> None:
        """
        Adds trace predictions a given cluster.
        :param args: The arguments to HGEN.
        :param state: The current state of HGEN.
        :param cluster_id: The id of the cluster.
        :param parent_ids: List of parents in the cluster.
        :param trace_predictions: All predictions across all clusters.
        :param trace_selections: Selected predictions across all clusters.
        :return: None (adds directly to trace predictions/selections).
        """
        children_ids = [a_id for a_id in state.get_cluster2artifacts(ids_only=True)[cluster_id]
                        if a_id in state.source_dataset.artifact_df]

        cluster_dir = FileUtil.safely_join_paths(HGenUtil.get_ranking_dir(state.export_dir), str(cluster_id))
        run_name = f"Cluster{cluster_id}: " + RankingArgs.get_run_name(args.source_type, children_ids,
                                                                       args.target_type, parent_ids)
        cluster_predictions = self._run_embedding_pipeline(args, state, run_name=run_name,
                                                           parent_ids=parent_ids, children_ids=children_ids,
                                                           export_dir=cluster_dir,
                                                           selection_method=None)

        link_selection_threshold = RankingUtil.calculate_threshold_from_std(cluster_predictions)
        cluster_selections = SelectByThresholdScaledAcrossAll.select(cluster_predictions, link_selection_threshold)

        parent2selections = RankingUtil.group_trace_predictions(cluster_selections, TraceKeys.parent_label())
        parent2predictions = RankingUtil.group_trace_predictions(cluster_predictions, TraceKeys.parent_label())
        for parent, parent_preds in parent2predictions.items():
            parent_selected_traces = parent2selections.get(parent, [])
            if len(parent_selected_traces) == 0 and not args.check_target_type_constraints(DocTypeConstraints.ONE_TARGET_PER_SOURCE):
                parent_selected_traces = self._trace_barren_parents(args, parent_preds)
            trace_selections.extend(parent_selected_traces)
        trace_predictions.extend(cluster_predictions)

    @staticmethod
    def _trace_barren_parents(args: HGenArgs, parent_preds: List[Trace]) -> List[Trace]:
        """
        Adds traces for any parents without children.
        :param args: The arguments to HGEN.
        :param parent_preds: All traces for the parent.
        :return: Trace selections for parents.
        """
        best_trace = sorted(parent_preds, key=lambda t: t[TraceKeys.SCORE], reverse=True)[0]
        lower_threshold = args.link_selection_threshold - 0.1
        if best_trace[TraceKeys.SCORE] >= lower_threshold:
            # grab all at lower threshold
            parent_selected_traces = SelectByThreshold.select(parent_preds, lower_threshold)
        else:
            parent_selected_traces = [best_trace]  # just grab the best one
        return parent_selected_traces

    @staticmethod
    def _trace_orphan_children(state: HGenState, trace_predictions: List[Trace], trace_selections: List[Trace]) -> None:
        """
        Traces any orphans to their top parent.
        :param state: The current state of HGen.
        :param trace_predictions: All predictions.
        :param trace_selections: Selected predictions.
        :return: None (adds directly to trace selections list).
        """
        child2selections = RankingUtil.group_trace_predictions(trace_selections, TraceKeys.child_label())
        orphans = set(state.source_dataset.artifact_df.index).difference(child2selections.keys())
        all_child_predictions = RankingUtil.group_trace_predictions(trace_predictions, TraceKeys.child_label(), sort_entries=True)
        selected_traces = [all_child_predictions[orphan][0] for orphan in orphans if orphan in all_child_predictions]
        trace_selections.extend(selected_traces)

    @staticmethod
    def _run_embedding_pipeline(args: HGenArgs, state: HGenState,
                                parent_ids: List, children_ids: List,
                                export_dir: str = None, **pipeline_args) -> List[Trace]:
        """
        Runs the embedding pipeline to obtain trace predictions
        :param args: The arguments to HGEN.
        :param state: The state of HGEN.
        :param parent_ids: The list of parent ids to trace.
        :param children_ids: The list of children ids to trace.
        :param export_dir: Directory to export to.
        :param pipeline_args: Additional arguments to the tracing pipeline.
        :return: The selected predictions from the pipeline.
        """
        ranking_args = RankingArgs(parent_ids=parent_ids,
                                   children_ids=children_ids,
                                   dataset=state.all_artifacts_dataset,
                                   types_to_trace=(args.source_type, args.target_type),
                                   export_dir=export_dir,
                                   generate_explanations=False,
                                   embeddings_manager=state.embedding_manager,
                                   **pipeline_args)
        ranking_state = RankingState()
        sort_children_step = SortChildrenStep()
        sort_children_step.run(ranking_args, ranking_state, verbose=False)
        selected_predictions = ranking_state.get_current_entries()
        return selected_predictions

    @staticmethod
    def _create_traces_from_references(id_to_related_children) -> List[EnumDict]:
        """
        Creates traces using the related sources from the previous step
        :param id_to_related_children: Dictionary mapping new artifact id to a list of related children
        :return: List of traces created from the related sources from the previous step
        """
        trace_predictions = []
        for p_id, related_children in id_to_related_children.items():
            for artifact in related_children:
                trace_predictions.append(
                    RankingUtil.create_entry(parent=p_id, child=artifact, score=RELATED_CHILDREN_SCORE))
        return trace_predictions

    @staticmethod
    def _weight_scores_with_related_children_predictions(trace_predictions: List[EnumDict],
                                                         id_to_related_children: Dict[str, Set]) -> List[EnumDict]:
        """
        Adjusts the score to reflect that an artifact was predicted to be related (through clustering or artifact gen step)
        :param trace_predictions: The list of trace predictions from ranking job
        :param id_to_related_children: A dictionary mapping the generated content id to the list of predicted relationships
        :return: The adjusted trace predictions
        """
        for trace in trace_predictions:
            child = trace[TraceKeys.child_label()]
            parent = trace[TraceKeys.parent_label()]
            if parent in id_to_related_children and child in id_to_related_children[parent]:
                alpha = WEIGHT_OF_PRED_RELATED_CHILDREN
                trace[TraceKeys.SCORE] = MathUtil.calculate_weighted_score(RELATED_CHILDREN_SCORE,
                                                                           trace[TraceKeys.SCORE], alpha)
        return trace_predictions
