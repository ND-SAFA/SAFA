from typing import List, Tuple, Dict

from tgen.common.util.dict_util import DictUtil
from tgen.common.logging.logger_manager import logger

from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import TraceKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.hgen.common.duplicate_detector import DuplicateDetector
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.pipeline.abstract_pipeline import AbstractPipelineStep
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

        new_artifact_map = state.new_artifact_dataset.artifact_df.to_map()
        new_artifact_embeddings_map = embeddings_manager.update_or_add_contents(new_artifact_map, create_embedding=True)
        new_artifact_ids = list(new_artifact_embeddings_map.keys())

        duplicate_detector = DuplicateDetector(embeddings_manager, duplicate_similarity_threshold=args.duplicate_similarity_threshold)
        duplicate_artifact_ids, duplicate_pairs = duplicate_detector.get_duplicates(new_artifact_ids)

        logger.info(f"Removing: {len(duplicate_artifact_ids)} duplicates.")

        selected_artifacts_df = ArtifactDataFrame(state.all_artifacts_dataset.artifact_df.to_dict("with_id_col"))
        selected_artifacts_df.remove_rows(duplicate_artifact_ids)
        state.selected_artifacts_dataset = PromptDataset(artifact_df=selected_artifacts_df,
                                                         project_summary=state.all_artifacts_dataset.project_summary)

        self._re_trace_duplicates(args, state, duplicate_artifact_ids, duplicate_pairs)

    @staticmethod
    def _re_trace_duplicates(args: HGenArgs, state: HGenState, duplicate_artifact_ids: List[str],
                             duplicate_pairs: List[Tuple]) -> None:
        """
        Re traces the children of a duplicate being removed to its potential dups
        :param args: The arguments to HGEN
        :param state: The current state of HGEN
        :param duplicate_artifact_ids: A list of duplicate artifact ids to remove
        :param duplicate_pairs: A list of pairs of duplicate artifacts
        :return: None
        """
        duplicate_map = DetectDuplicateArtifactsStep._create_duplicate_map(duplicate_pairs)
        trace_predictions, selected_predictions, existing_traces = [], [], set()
        selected_artifact_pairs = {(trace[TraceKeys.parent_label()], trace[TraceKeys.child_label()])
                                   for trace in state.selected_predictions}
        state.embedding_manager.update_or_add_contents(content_map=state.all_artifacts_dataset.artifact_df.to_map())
        for trace in state.trace_predictions:
            parent = trace[TraceKeys.parent_label()]
            child = trace[TraceKeys.child_label()]
            if parent in duplicate_artifact_ids:
                potential_parents = duplicate_map[parent].difference(duplicate_artifact_ids)
                if not potential_parents:
                    continue
                sorted_parents, sorted_scores = EmbeddingSorter.sort([child], potential_parents,
                                                                     embedding_manager=state.embedding_manager,
                                                                     return_scores=True)[child]
                top_parent, top_parent_score = sorted_parents[0], sorted_scores[0]
                if top_parent_score < args.link_selection_threshold:
                    continue  # discard trace entirely
                trace[TraceKeys.parent_label()] = top_parent
            pair = (trace[TraceKeys.parent_label()], child)
            if pair not in existing_traces:
                trace_predictions.append(trace)
                existing_traces.add(pair)
                if (parent, child) in selected_artifact_pairs:
                    selected_predictions.append(trace)
        state.trace_predictions = trace_predictions
        state.selected_predictions = selected_predictions

    @staticmethod
    def _create_duplicate_map(duplicate_pairs: List[Tuple]) -> Dict:
        """
        Creates a map of an artifact id to a set of its potential dups
        :param duplicate_pairs: A list of tuples containing pairs of artifacts flagged as dups
        :return: A map of an artifact id to a set of its potential dups
        """
        duplicate_map = {}
        for (a1, a2) in duplicate_pairs:
            DictUtil.set_or_append_item(duplicate_map, a1, a2, iterable_type=set)
            DictUtil.set_or_append_item(duplicate_map, a2, a1, iterable_type=set)
        return duplicate_map
