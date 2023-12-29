from typing import Dict, List, Set

from tgen.common.constants.artifact_summary_constants import USE_NL_SUMMARY_EMBEDDINGS
from tgen.common.constants.hgen_constants import FIRST_PASS_LINK_THRESHOLD
from tgen.common.logging.logger_manager import logger
from tgen.common.util.dict_util import DictUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import TraceKeys, ArtifactKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.hgen.common.duplicate_detector import DuplicateDetector
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.tracing.ranking.sorters.embedding_sorter import EmbeddingSorter


class DetectDuplicateArtifactsStep(AbstractPipelineStep[HGenArgs, HGenState]):

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Removes duplicate generated artifacts.
        :param args: The arguments to HGEN pipeline.
        :param state: The state of the
        :return: None
        """

        embeddings_manager = state.embedding_manager

        new_artifact_map = state.new_artifact_dataset.artifact_df.to_map(use_code_summary_only=not USE_NL_SUMMARY_EMBEDDINGS)
        new_artifact_embeddings_map = embeddings_manager.update_or_add_contents(new_artifact_map, create_embedding=True)
        new_artifact_ids = list(new_artifact_embeddings_map.keys())

        duplicate_detector = DuplicateDetector(embeddings_manager, duplicate_similarity_threshold=args.duplicate_similarity_threshold)
        duplicate_artifact_ids, duplicate_map = duplicate_detector.get_duplicates(new_artifact_ids)
        duplicate_map = self._remove_duplicates_from_same_cluster(duplicate_artifact_ids, duplicate_map, state)
        logger.info(f"Removing: {len(duplicate_artifact_ids)} duplicates.")

        selected_artifacts_df = ArtifactDataFrame(state.all_artifacts_dataset.artifact_df.to_dict("list", index=True))
        selected_artifacts_df.remove_rows(duplicate_artifact_ids)
        state.selected_artifacts_dataset = PromptDataset(artifact_df=selected_artifacts_df,
                                                         project_summary=state.all_artifacts_dataset.project_summary)

        self._re_trace_duplicates(state, duplicate_artifact_ids, duplicate_map)

    @staticmethod
    def _remove_duplicates_from_same_cluster(duplicate_artifact_ids: Set[str], duplicate_map: Dict[str, Set[str]],
                                             state: HGenState) -> Dict[str, Set[str]]:
        """
        Removes duplicates that originated from the same cluster because less likely to be real duplicates (just related).
        :param duplicate_artifact_ids: Set of all selected duplicate ids.
        :param duplicate_map: The map of identified duplicate families.
        :param state: The current state of HGen.
        :return: The refined duplicate map.
        """
        generation2cluster = DictUtil.flip(state.get_cluster2generation())
        refined_duplicate_map = {}
        for a_id, duplicates in duplicate_map.items():
            content = state.new_artifact_dataset.artifact_df.get_artifact(a_id)[ArtifactKeys.CONTENT]
            cluster = generation2cluster[content]
            refined_duplicates = set()
            for dup_id in duplicates:
                dup_content = state.new_artifact_dataset.artifact_df.get_artifact(dup_id)[ArtifactKeys.CONTENT]
                if generation2cluster[dup_content] != cluster:
                    refined_duplicates.add(dup_id)
            if refined_duplicates:
                refined_duplicate_map[a_id] = refined_duplicates
            elif a_id in duplicate_artifact_ids:
                duplicate_artifact_ids.remove(a_id)
        return refined_duplicate_map

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

            if parent in duplicate_artifact_ids:
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
        sorted_parents, sorted_scores = EmbeddingSorter.sort([artifact_id], potential_parents,
                                                             embedding_manager=embeddings_manager,
                                                             return_scores=True)[artifact_id]
        top_parent, top_parent_score = sorted_parents[0], sorted_scores[0]
        if top_parent_score < min_score:
            return None
        return top_parent
