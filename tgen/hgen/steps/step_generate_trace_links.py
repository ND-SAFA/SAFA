from typing import Dict, List, Set, Tuple

from tgen.common.constants.artifact_summary_constants import USE_NL_SUMMARY_EMBEDDINGS
from tgen.common.constants.hgen_constants import FIRST_PASS_LINK_THRESHOLD, RELATED_CHILDREN_SCORE, \
    WEIGHT_OF_PRED_RELATED_CHILDREN
from tgen.common.logging.logger_manager import logger
from tgen.common.objects.trace import Trace
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.common.util.math_util import MathUtil
from tgen.data.keys.structure_keys import TraceKeys
from tgen.hgen.common.hgen_util import HGenUtil
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.selectors.select_by_threshold import SelectByThreshold
from tgen.tracing.ranking.steps.sort_children_step import SortChildrenStep


class GenerateTraceLinksStep(AbstractPipelineStep[HGenArgs, HGenState]):

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Generates trace links between the new generated artifacts and the source artifacts
        :param state: The current state of hgen at this point in time
        :param args: The arguments and current state of HGEN.
        :return: None
        """

        if not args.generate_trace_links:
            state.trace_predictions = self._create_traces_from_references(state.id_to_related_children)
            state.selected_predictions = state.trace_predictions
            return

        logger.info(f"Predicting links between {args.target_type} and {args.source_layer_ids}\n")

        if args.perform_clustering:
            trace_predictions, selected_predictions = self._trace_artifacts_in_cluster_to_generated_parents(args, state)
        else:
            trace_predictions = self._run_tracing_job_on_all_artifacts(args, state)
            trace_predictions = self._weight_scores_with_related_children_predictions(trace_predictions,
                                                                                      state.id_to_related_children)
            selected_predictions = SelectByThreshold.select(trace_predictions, args.link_selection_threshold)
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
        run_name = RankingArgs.get_run_name(args.source_type, children_ids, args.target_type, parent_ids)
        pipeline_args = RankingArgs(run_name=run_name, parent_ids=parent_ids,
                                    children_ids=children_ids,
                                    dataset=state.all_artifacts_dataset,
                                    types_to_trace=(args.source_type, args.target_type),
                                    export_dir=HGenUtil.get_ranking_dir(state.export_dir),
                                    generate_explanations=args.generate_explanations,
                                    link_threshold=FIRST_PASS_LINK_THRESHOLD)
        selected_entries = self._run_embedding_pipeline(pipeline_args)
        trace_predictions: List[EnumDict] = selected_entries
        return trace_predictions

    def _trace_artifacts_in_cluster_to_generated_parents(self, args: HGenArgs, state: HGenState) -> Tuple[List[Trace], List[Trace]]:
        """
        Generates links between the artifacts in a cluster and the parent artifact generated from the cluster artifacts
        :param args: The arguments to HGen
        :param state: The current state of HGen
        :return: The trace predictions for the clusters
        """
        new_artifact_map = state.new_artifact_dataset.artifact_df.to_map()
        trace_predictions, selected_traces = [], []
        generation2id = {content: a_id for a_id, content in new_artifact_map.items()}
        state.all_artifacts_dataset.project_summary = args.dataset.project_summary
        new_artifact_map = state.all_artifacts_dataset.artifact_df.to_map(use_code_summary_only=not USE_NL_SUMMARY_EMBEDDINGS)
        state.embedding_manager.update_or_add_contents(new_artifact_map)
        subset_ids = list({a_id for a_ids in state.cluster2artifacts.values() for a_id in a_ids})
        subset_ids += list(state.new_artifact_dataset.artifact_df.index)
        state.embedding_manager.create_artifact_embeddings(artifact_ids=subset_ids)
        pipeline_kwargs = dict(dataset=state.all_artifacts_dataset, selection_method=None,
                               types_to_trace=(args.source_type, args.target_type), generate_explanations=False,
                               embeddings_manager=state.embedding_manager)

        orphans = state.original_dataset.trace_dataset.trace_df.get_orphans() if state.original_dataset.trace_dataset else set()
        for cluster_id in state.cluster_dataset.artifact_df.index:
            generations = state.cluster2generation.get(cluster_id)
            parent_ids = [generation2id[generation] for generation in generations if
                          generation in generation2id]  # ignores if dup deleted already
            if len(parent_ids) == 0:
                continue
            children_ids = [a_id for a_id in state.cluster2artifacts[cluster_id]
                            if a_id in state.source_dataset.artifact_df
                            or a_id in orphans]
            cluster_dir = FileUtil.safely_join_paths(HGenUtil.get_ranking_dir(state.export_dir), str(cluster_id))
            run_name = f"Cluster{cluster_id}: " + RankingArgs.get_run_name(args.source_type, children_ids,
                                                                           args.target_type, parent_ids)
            pipeline_args = RankingArgs(run_name=run_name, parent_ids=parent_ids, children_ids=children_ids,
                                        export_dir=cluster_dir,
                                        **pipeline_kwargs)
            cluster_predictions = self._run_embedding_pipeline(pipeline_args)
            parent2predictions = RankingUtil.group_trace_predictions(cluster_predictions, TraceKeys.parent_label())
            for parent, parent_preds in parent2predictions.items():
                parent_selected_traces = SelectByThreshold.select(parent_preds, FIRST_PASS_LINK_THRESHOLD)
                if len(parent_selected_traces) == 0:
                    parent_selected_traces = sorted(parent_preds, key=lambda t: t[TraceKeys.SCORE], reverse=True)[:1]
                selected_traces.extend(parent_selected_traces)
            trace_predictions.extend(cluster_predictions)
        return trace_predictions, selected_traces

    @staticmethod
    def _run_embedding_pipeline(ranking_args: RankingArgs) -> List[Trace]:
        """
        Runs the embedding pipeline to obtain trace predictions
        :param ranking_args: The arguments to the ranking pipeline
        :return: The selected predictions from the pipeline
        """
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
