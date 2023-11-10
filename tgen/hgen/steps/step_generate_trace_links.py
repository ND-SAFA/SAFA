import os
from typing import Dict, List, Set, Tuple

from tgen.common.constants.hgen_constants import FIRST_PASS_LINK_THRESHOLD, RELATED_CHILDREN_SCORE, \
    WEIGHT_OF_PRED_RELATED_CHILDREN
from tgen.common.objects.trace import Trace
from tgen.common.util.dict_util import DictUtil
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.common.logging.logger_manager import logger
from tgen.common.util.math_util import MathUtil
from tgen.data.keys.structure_keys import ArtifactKeys, TraceKeys
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.jobs.tracing_jobs.ranking_job import RankingJob
from tgen.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.embedding_ranking_pipeline import EmbeddingRankingPipeline
from tgen.tracing.ranking.selectors.select_by_threshold import SelectByThreshold
from tgen.tracing.ranking.steps.create_explanations_step import CreateExplanationsStep


class GenerateTraceLinksStep(AbstractPipelineStep[HGenArgs, HGenState]):

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Generates trace links between the new generated artifacts and the source artifacts
        :param state: The current state of hgen at this point in time
        :param args: The arguments and current state of HGEN.
        :return: None
        """

        if not args.generate_trace_links:
            state.trace_predictions = self._create_traces_from_generation_predictions(state.id_to_related_children)
            state.selected_predictions = state.trace_predictions
            return

        logger.info(f"Predicting links between {args.target_type} and {args.source_layer_id}\n")

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
        children_ids = list(state.all_artifacts_dataset.artifact_df.get_type(args.source_layer_id).index)
        parent_ids = list(state.all_artifacts_dataset.artifact_df.get_type(args.target_type).index)
        run_name = RankingJob.get_run_name(args.source_type, children_ids, args.target_type, parent_ids)
        pipeline_args = RankingArgs(run_name=run_name, parent_ids=parent_ids,
                                    children_ids=children_ids,
                                    dataset=state.all_artifacts_dataset,
                                    types_to_trace=(args.source_type, args.target_type),
                                    export_dir=self._get_ranking_dir(state.export_dir),
                                    generate_explanations=args.generate_explanations,
                                    link_threshold=FIRST_PASS_LINK_THRESHOLD)
        selected_entries = self._run_embedding_pipeline(pipeline_args, state)
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
        pipeline_kwargs = dict(dataset=state.all_artifacts_dataset, selection_method=None,
                               types_to_trace=(args.source_type, args.target_type), generate_explanations=False)
        for cluster_id in state.cluster_dataset.artifact_df.index:
            generations = state.cluster2generation.get(cluster_id)
            parent_ids = [generation2id[generation] for generation in generations if
                          generation in generation2id]  # ignores if dup deleted already
            if len(parent_ids) == 0:
                continue
            children_ids = [a[ArtifactKeys.ID] for a in state.id_to_cluster_artifacts[cluster_id]]
            cluster_dir = FileUtil.safely_join_paths(self._get_ranking_dir(state.export_dir), str(cluster_id))
            run_name = f"Cluster{cluster_id}: " + RankingJob.get_run_name(args.source_type, children_ids,
                                                                          args.target_type, parent_ids)
            pipeline_args = RankingArgs(run_name=run_name, parent_ids=parent_ids, children_ids=children_ids, export_dir=cluster_dir,
                                        **pipeline_kwargs)
            cluster_predictions = self._run_embedding_pipeline(pipeline_args, state)
            parent2predictions = RankingUtil.group_trace_predictions(cluster_predictions, TraceKeys.parent_label())
            for parent, parent_preds in parent2predictions.items():
                parent_selected_traces = SelectByThreshold.select(parent_preds, FIRST_PASS_LINK_THRESHOLD)
                if len(parent_selected_traces) == 0:
                    parent_selected_traces = sorted(parent_preds, key=lambda t: t[TraceKeys.SCORE], reverse=True)[:1]
                selected_traces.extend(parent_selected_traces)
            trace_predictions.extend(cluster_predictions)
        if args.generate_explanations:
            selected_traces = self._generate_explanations(selected_traces, state,
                                                          export_dir=FileUtil.safely_join_paths(
                                                              GenerateTraceLinksStep._get_ranking_dir(state.export_dir),
                                                              "explanations"
                                                          ),
                                                          **pipeline_kwargs)
        return trace_predictions, selected_traces

    @staticmethod
    def _run_embedding_pipeline(pipeline_args: RankingArgs, hgen_state: HGenState) -> List[Trace]:
        """
        Runs the embedding pipeline to obtain trace predictions
        :param pipeline_args: The arguments to the ranking pipeline
        :param hgen_state: The current hgen state
        :return: The selected predictions from the pipeline
        """
        pipeline = EmbeddingRankingPipeline(pipeline_args, embedding_manager=hgen_state.embedding_manager)
        pipeline.run()
        hgen_state.update_total_costs_from_state(pipeline.state)
        hgen_state.all_artifacts_dataset.project_summary = pipeline.state.project_summary
        selected_predictions = pipeline.state.selected_entries
        return selected_predictions

    @staticmethod
    def _create_traces_from_generation_predictions(id_to_related_children) -> List[EnumDict]:
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
    def _generate_explanations(selected_traces: List[Trace], state: HGenState, **pipeline_kwargs) -> List[Trace]:
        """
        Generates explanations for each selected trace
        :param selected_traces: List of traces that have been selected
        :param pipeline_kwargs: Additional pipeline arguments
        :param state: The current state of HGEN
        :return: The list of traces with explanations
        """
        pipeline_kwargs = DictUtil.update_kwarg_values(pipeline_kwargs, generate_explanations=True)
        pipeline_args = RankingArgs(run_name="explanations", parent_ids=[], children_ids=[],
                                    weight_of_explanation_scores=0,
                                    **pipeline_kwargs)
        pipeline_args.update_llm_managers_with_state(state)
        pipeline_state = RankingState(candidate_entries=selected_traces)
        CreateExplanationsStep().run(pipeline_args, pipeline_state)
        selected_traces = pipeline_state.get_current_entries()
        return selected_traces

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

    @staticmethod
    def _get_ranking_dir(directory: str) -> str:
        """
        Get the directory for ranking job
        :param directory: The main directory used by hgen
        :return: The full path
        """
        return FileUtil.safely_join_paths(directory, "ranking")
