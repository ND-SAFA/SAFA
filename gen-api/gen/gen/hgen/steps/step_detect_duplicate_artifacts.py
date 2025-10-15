from collections import Counter
from typing import Dict, List, Set, Tuple

from gen_common.constants.model_constants import USE_NL_SUMMARY_EMBEDDINGS
from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.keys.structure_keys import TraceKeys
from gen_common.data.objects.trace import Trace
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep
from gen_common.traceability.ranking.sorters.transformer_sorter import TransformerSorter
from gen_common.traceability.ranking.trace_selectors.select_by_threshold import SelectByThreshold
from gen_common.traceability.relationship_manager.embeddings_manager import EmbeddingsManager
from gen_common.util.dict_util import DictUtil
from gen_common.util.ranking_util import RankingUtil

from gen.constants.hgen_constants import FIRST_PASS_LINK_THRESHOLD
from gen.hgen.common.duplicate_detector import DuplicateDetector, DuplicateType
from gen.hgen.hgen_args import HGenArgs
from gen.hgen.hgen_state import HGenState


class DetectDuplicateArtifactsStep(AbstractPipelineStep[HGenArgs, HGenState]):

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Removes duplicate generated artifacts.
        :param args: The arguments to HGEN pipeline.
        :param state: The state of the
        :return: None
        """
        if not args.perform_clustering or not args.detect_duplicates:
            state.selected_artifacts_dataset = state.all_artifacts_dataset
            return

        embeddings_manager = state.embedding_manager

        new_artifact_map = state.new_artifact_dataset.artifact_df.to_map(use_code_summary_only=not USE_NL_SUMMARY_EMBEDDINGS)
        embeddings_manager.update_or_add_contents(new_artifact_map)

        duplicate_detector = DuplicateDetector(embeddings_manager,
                                               duplicate_similarity_threshold=args.duplicate_similarity_threshold)
        duplicate_artifact_ids, duplicate_map = duplicate_detector.get_duplicates(
            state.new_artifact_dataset.artifact_df, original_clusters_to_contents=state.get_cluster2generation(),
            duplicate_type=DuplicateType.INTER_CLUSTER)

        strong_duplicates, _ = self._allow_tracing_between_dups(state, duplicate_map)
        duplicate_artifact_ids = {a for a in duplicate_artifact_ids if a in strong_duplicates}
        selected_artifacts_df = ArtifactDataFrame(state.all_artifacts_dataset.artifact_df.to_dict("list", index=True))
        selected_artifacts_df.remove_rows(duplicate_artifact_ids)
        state.selected_artifacts_dataset = PromptDataset(artifact_df=selected_artifacts_df,
                                                         project_summary=state.all_artifacts_dataset.project_summary)
        state.trace_predictions = self._remove_traces(state.trace_predictions, duplicate_artifact_ids)
        state.selected_predictions = self._remove_traces(state.selected_predictions, duplicate_artifact_ids)

    @staticmethod
    def _remove_traces(predictions: List[Trace], duplicate_artifact_ids: Set[str]) -> List[Trace]:
        """
        Removes the traces that contain a duplicate artifact id.
        :param predictions: List of the predictions to remove from.
        :param duplicate_artifact_ids: The artifact ids to remove.
        :return: The list of traces without any containing duplicate artifacts.
        """
        return [pred for pred in predictions
                if pred[TraceKeys.parent_label()] not in duplicate_artifact_ids]

    @staticmethod
    def _allow_tracing_between_dups(state: HGenState, duplicate_map: Dict[str, Set[str]]) -> Tuple[
        Dict[str, Set], Dict[str, List[Trace]]]:
        """
        Re traces the children of a duplicate being removed to its potential dups
        :param state: The current state of HGEN
        :param duplicate_map:  A dictionary mapping dup id to possible duplicates.
        :return: A dictionary mapping dup id to its confirmed duplicates.
        """
        content_map = state.all_artifacts_dataset.artifact_df.to_map(use_code_summary_only=not USE_NL_SUMMARY_EMBEDDINGS)
        state.embedding_manager.update_or_add_contents(content_map=content_map)
        state.embedding_manager.create_embeddings(list(content_map.keys()))
        parent2selections = RankingUtil.group_trace_predictions(state.selected_predictions, TraceKeys.parent_label())
        strong_duplicates = {}
        dup2links = {}
        for dup_id, related_dups in duplicate_map.items():
            selected_traces = parent2selections[dup_id]
            candidate_children = [trace[TraceKeys.child_label()] for trace in selected_traces]
            parent_rankings = TransformerSorter.sort([dup_id, *related_dups], candidate_children,
                                                     relationship_manager=state.embedding_manager,
                                                     return_scores=True)
            dup_scores = parent_rankings.pop(dup_id)
            baseline = {child: score for child, score in zip(dup_scores[0], dup_scores[1])}

            predictions = [RankingUtil.create_entry(p_id, c_id, score) for p_id, preds in parent_rankings.items()
                           for c_id, score in zip(preds[0], preds[1])]
            child2traces = RankingUtil.group_trace_predictions(predictions, TraceKeys.child_label())

            dup_selections = []
            for child, traces in child2traces.items():
                selections = SelectByThreshold.select(traces, baseline[child] - 0.15)
                dup_selections.extend(selections)
            dup2selected = RankingUtil.group_trace_predictions(dup_selections, TraceKeys.parent_label())
            confirmed_dups = set()
            for dup, selected in dup2selected.items():
                if len(selected) == len(selected_traces):
                    confirmed_dups.add(dup)
                    DictUtil.set_or_append_item(dup2links, dup_id, selected)
                state.selected_predictions.extend(selected)
            if len(confirmed_dups):
                strong_duplicates[dup_id] = confirmed_dups
        dup_counter = Counter([d for dups in strong_duplicates.values() for d in dups])
        selected_duplicates = DuplicateDetector.find_most_duplicated_artifacts(dup_counter, strong_duplicates)
        return selected_duplicates, dup2links

    @staticmethod
    def _re_trace_duplicates(state: HGenState, duplicate_artifact_ids: Set[str], duplicate_map: Dict[str, Set[str]]) -> None:
        """
        Re traces the children of a duplicate being removed to its potential dups
        :param state: The current state of HGEN
        :param duplicate_artifact_ids: A list of duplicate artifact ids to remove
        :param duplicate_map: A list of pairs of duplicate artifacts
        :return: None
        """
        trace_predictions, selected_predictions, existing_traces = [], [], set()
        selected_artifact_pairs = {(trace[TraceKeys.parent_label()], trace[TraceKeys.child_label()])
                                   for trace in state.selected_predictions}
        content_map = state.all_artifacts_dataset.artifact_df.to_map(use_code_summary_only=not USE_NL_SUMMARY_EMBEDDINGS)
        state.embedding_manager.update_or_add_contents(content_map=content_map)
        for trace in state.trace_predictions:
            parent_key = TraceKeys.parent_label()

            parent = trace[parent_key]
            child = trace[TraceKeys.child_label()]

            if parent in duplicate_map:
                potential_parents = duplicate_map[parent].difference(duplicate_artifact_ids)
                if not potential_parents:
                    continue
                new_parent = DetectDuplicateArtifactsStep.get_top_parent(child,
                                                                         potential_parents,
                                                                         state.embedding_manager,
                                                                         FIRST_PASS_LINK_THRESHOLD)
                if new_parent is None:
                    continue  # discard trace entirely
                trace[parent_key] = new_parent

            pair = (trace[parent_key], child)
            if pair not in existing_traces:
                existing_traces.add(pair)
                trace_predictions.append(trace)
                if (parent, child) in selected_artifact_pairs:
                    selected_predictions.append(trace)

        state.trace_predictions = trace_predictions
        state.selected_predictions = selected_predictions

    @staticmethod
    def get_top_parent(artifact_id: str, potential_parents: List[str], embeddings_manager: EmbeddingsManager, min_score: float):
        """
        Returns the most similar parent to the given artifact.
        :param artifact_id: ID of artifact to calculate similarity between.
        :param potential_parents: IDs of potential parents.
        :param embeddings_manager: Contains the artifact embeddings.
        :param min_score: The minimum similarity score to allow.
        :return: The most similar parent, if its score reaches a minimum threshold.
        """
        sorted_parents, sorted_scores = TransformerSorter.sort([artifact_id], potential_parents,
                                                               embedding_manager=embeddings_manager,
                                                               return_scores=True)[artifact_id]
        top_parent, top_parent_score = sorted_parents[0], sorted_scores[0]
        return top_parent
