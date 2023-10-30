import os
from typing import Dict, List, Set, Tuple

from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.constants.hgen_constants import FIRST_PASS_LINK_THRESHOLD, RELATED_CHILDREN_SCORE, \
    WEIGHT_OF_PRED_RELATED_CHILDREN
from tgen.common.objects.trace import Trace
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.math_util import MathUtil
from tgen.common.util.status import Status
from tgen.data.keys.structure_keys import ArtifactKeys, TraceKeys
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.jobs.tracing_jobs.ranking_job import RankingJob
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.embedding_ranking_pipeline import EmbeddingRankingPipeline
from tgen.tracing.ranking.selectors.select_by_threshold import SelectByThreshold
from tgen.tracing.ranking.supported_ranking_pipelines import SupportedRankingPipelines


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
            return

        logger.info(f"Predicting links between {args.target_type} and {args.source_layer_id}\n")

        if args.perform_clustering:
            trace_predictions, selected_predictions = self._trace_artifacts_in_cluster_to_generated_parents(args, state)
            self.place_orphans_in_homes(args, state, trace_predictions, selected_predictions)
        else:
            trace_predictions = self._run_tracing_job_on_all_artifacts(args, state)
            trace_predictions = self._weight_scores_with_related_children_predictions(trace_predictions,
                                                                                      state.id_to_related_children)
            selected_predictions = SelectByThreshold.select(trace_predictions, args.link_selection_threshold)
        state.selected_predictions = selected_predictions
        state.trace_predictions = trace_predictions

    @staticmethod
    def place_orphans_in_homes(args: HGenArgs,
                               state: HGenState,
                               trace_predictions: List[Trace],
                               trace_selections: List[Trace]) -> None:
        all_children_ids = list(state.all_artifacts_dataset.artifact_df.get_type(args.source_layer_id).index)
        all_parent_ids = list(state.all_artifacts_dataset.artifact_df.get_type(args.target_type).index)

        child2predictions = RankingUtil.group_trace_predictions(trace_predictions, TraceKeys.child_label())
        child2selected = RankingUtil.group_trace_predictions(trace_selections, TraceKeys.child_label())

        orphans = set()
        for child in all_children_ids:
            predicted_child_links = child2predictions.get(child, [])
            selected_child_links = child2selected.get(child, [])
            if len(selected_child_links) == 0:
                if len(predicted_child_links) == 0:
                    orphans.add(child)
                else:
                    all_child_predictions = sorted(predicted_child_links, key=lambda t: t[TraceKeys.SCORE], reverse=True)
                    trace_selections.append(all_child_predictions[0])

        run_name = "Placing Orphans in Homes"
        export_dir = os.path.join(args.export_dir, "orphan_ranking")
        pipeline_args = RankingArgs(run_name=run_name,
                                    dataset=state.all_artifacts_dataset,
                                    parent_ids=all_parent_ids,
                                    children_ids=list(orphans),
                                    export_dir=export_dir,
                                    types_to_trace=(args.source_type, args.target_type),
                                    generate_explanations=False,  # TODO make this a hgen arg
                                    selection_method=None)
        pipeline = EmbeddingRankingPipeline(pipeline_args, embedding_manager=state.embedding_manager)
        pipeline.run()

        orphan2predictions = RankingUtil.group_trace_predictions(pipeline.state.selected_entries, TraceKeys.child_label())
        for orphan_id, orphan_preds in orphan2predictions.items():
            top_prediction = sorted(orphan_preds, key=lambda t: t[TraceKeys.SCORE], reverse=True)[0]
            trace_selections.append(top_prediction)

    def _run_tracing_job_on_all_artifacts(self, args: HGenArgs, state: HGenState) -> List[EnumDict]:
        """
        Runs a ranking job for all candidate links between the children and generated parents
        :param args: The arguments to HGen
        :param state: The current state of HGen
        :return: The trace predictions for all candidates (that were not filtered)
        """
        tracing_job = RankingJob(dataset=state.all_artifacts_dataset,
                                 layer_ids=(args.target_type, args.source_layer_id),  # parent, child
                                 export_dir=self._get_ranking_dir(state.export_dir),
                                 load_dir=self._get_ranking_dir(args.load_dir),
                                 ranking_pipeline=SupportedRankingPipelines.EMBEDDING,
                                 link_threshold=FIRST_PASS_LINK_THRESHOLD)
        result = tracing_job.run()
        if result.status != Status.SUCCESS:
            raise Exception(f"Trace link generation failed: {result.body}")
        trace_predictions: List[EnumDict] = result.body.prediction_entries
        return trace_predictions

    def _trace_artifacts_in_cluster_to_generated_parents(self, args: HGenArgs, state: HGenState) -> Tuple[List[Trace], List[Trace]]:
        """
        Generates links between the artifacts in a cluster and the parent artifact generated from the cluster artifacts
        :param args: The arguments to HGen
        :param state: The current state of HGen
        :param generated_parents_df: Contains the parent content that aws generated generated
        :return: The trace predictions for the clusters
        """
        new_artifact_map = state.new_artifact_dataset.artifact_df.to_map()
        trace_predictions, selected_traces = [], []
        generation2id = {content: a_id for a_id, content in new_artifact_map.items()}
        state.all_artifacts_dataset.project_summary = args.dataset.project_summary
        for cluster_id in state.cluster_dataset.artifact_df.index:
            generations = state.cluster2generation.get(cluster_id)
            parent_ids = [generation2id[generation] for generation in generations if
                          generation in generation2id]  # ignores if dup deleted already
            if len(parent_ids) == 0:  # TODO: Filter out cluster ids that get removed
                continue
            children_ids = [a[ArtifactKeys.ID] for a in state.id_to_cluster_artifacts[cluster_id]]
            cluster_dir = os.path.join(self._get_ranking_dir(state.export_dir),
                                       str(cluster_id)) if state.export_dir else EMPTY_STRING
            run_name = f"Cluster{cluster_id}: " + RankingJob.get_run_name(args.source_type, children_ids,
                                                                          args.target_type, parent_ids)
            pipeline_args = RankingArgs(run_name=run_name,
                                        dataset=state.all_artifacts_dataset,
                                        parent_ids=parent_ids,
                                        children_ids=children_ids,
                                        export_dir=cluster_dir,
                                        types_to_trace=(args.source_type, args.target_type),
                                        generate_explanations=False,  # TODO make this a hgen arg
                                        selection_method=None)
            pipeline = EmbeddingRankingPipeline(pipeline_args, embedding_manager=state.embedding_manager)
            pipeline.run()
            state.all_artifacts_dataset.project_summary = pipeline.state.project_summary
            cluster_predictions = pipeline.state.selected_entries
            parent2predictions = RankingUtil.group_trace_predictions(cluster_predictions, TraceKeys.parent_label())
            for parent, parent_preds in parent2predictions.items():
                parent_selected_traces = SelectByThreshold.select(parent_preds, FIRST_PASS_LINK_THRESHOLD)
                if len(parent_selected_traces) == 0:
                    parent_selected_traces = sorted(parent_preds, key=lambda t: t[TraceKeys.SCORE], reverse=True)[:1]
                selected_traces.extend(parent_selected_traces)
            trace_predictions.extend(cluster_predictions)
        return trace_predictions, selected_traces

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
        return os.path.join(directory, "ranking") if directory else EMPTY_STRING
