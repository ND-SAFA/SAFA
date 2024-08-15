from copy import deepcopy
from typing import Dict, List

from common_resources.data.keys.structure_keys import TraceKeys
from common_resources.tools.constants.model_constants import USE_NL_SUMMARY_EMBEDDINGS
from common_resources.tools.util.enum_util import EnumDict
from common_resources.traceability.relationship_manager.embeddings_manager import EmbeddingsManager

from tgen.common.constants.ranking_constants import PRE_SORTED_SCORE
from tgen.common.util.artifact_df_util import chunk_artifact_df
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.sorters.i_sorter import iSorter
from tgen.tracing.ranking.sorters.supported_sorters import SupportedSorter


class SortChildrenStep(AbstractPipelineStep[RankingArgs, RankingState]):

    def _run(self, args: RankingArgs, state: RankingState) -> None:
        """
        Sorts the children for each parent according to specified sorting function.
        :param args: The ranking arguments to the pipeline.
        :param state: The state of the current pipeline.
        :return: NOne
        """
        children_ids = deepcopy(args.children_ids)
        if args.use_chunks:
            chunk_artifact_df(args.dataset.artifact_df)
            args.dataset.artifact_df.chunk_artifact_df()
            chunk_ids = list(args.dataset.artifact_df.get_chunk_map(orig_artifact_ids=set(args.children_ids)).keys())
            children_ids += chunk_ids
        state.artifact_map = args.dataset.artifact_df.to_map(use_code_summary_only=not USE_NL_SUMMARY_EMBEDDINGS,
                                                             include_chunks=args.use_chunks)
        use_sorter = args.sorter is not None
        use_pre_ranked = args.pre_sorted_parent2children is not None

        if use_pre_ranked:
            n_parents = len(args.parent_ids)
            n_children = len(children_ids)
            parent2rankings = {p: list(children) for p, children in args.pre_sorted_parent2children.items()}
            state.sorted_parent2children = {p: [RankingUtil.create_entry(p, c, score=PRE_SORTED_SCORE) for c in rankings]
                                            for p, rankings in parent2rankings.items()}
            add_sorted_children = len(args.pre_sorted_parent2children) < n_parents or any(
                [len(v) < n_children for v in args.pre_sorted_parent2children.values()])
            if add_sorted_children:
                state.sorted_parent2children = self.add_missing_children(args, state)
        elif use_sorter:
            parent_map = self.create_sorted_parent_map(args, state, children_ids)
            state.sorted_parent2children = parent_map
        else:
            raise AssertionError("Expected sorter or parent2children to be defined.")

    @staticmethod
    def add_missing_children(args: RankingArgs, state: RankingState) -> Dict[str, List[EnumDict]]:
        """
        Adds any children missing in args.parent2children in the order defined by sorter.
        :param args: The ranking pipeline arguments.
        :param state: The current state of the ranking pipeline
        :return: None (modified in place)
        """
        original_max_content = args.max_context_artifacts
        args.max_context_artifacts = None
        sorted_parent_map = SortChildrenStep.create_sorted_parent_map(args, state)
        final_parent_map = {}
        for p, sorted_children in sorted_parent_map.items():
            defined_children = state.sorted_parent2children.get(p, [])
            defined_children_set = set(c[TraceKeys.child_label()] for c in defined_children)
            missing_children = [c for c in sorted_children if c[TraceKeys.child_label()] not in defined_children_set]
            final_parent_map[p] = defined_children + missing_children
        args.max_context_artifacts = original_max_content
        return final_parent_map

    @staticmethod
    def create_sorted_parent_map(args: RankingArgs, state: RankingState, children_ids: List[str] = None) -> Dict[str, List]:
        """
        Sorts the children artifacts against each parent, resulting in a list of children from most to least similar.
        :param args: The ranking pipeline arguments.
        :param state: The current state of the ranking pipeline.
        :param children_ids: List of the children ids.
        :return: The map of parent IDs to sorted children IDs.
        """
        children_ids = args.children_ids if not children_ids else children_ids
        sorter: iSorter = SupportedSorter.get_value(args.sorter.upper()) if isinstance(args.sorter, str) else args.sorter.value
        if args.embeddings_manager:
            args.embeddings_manager.update_or_add_contents(state.artifact_map)
        else:
            args.embeddings_manager = EmbeddingsManager(content_map=state.artifact_map, model_name=args.embedding_model_name)

        # TODO: use enum to differentiate?
        relationship_manager = args.embeddings_manager if args.embeddings_manager else args.cross_encoder_manager
        parent2rankings = sorter.sort(args.parent_ids, children_ids, artifact_map=state.artifact_map,
                                      relationship_manager=relationship_manager, return_scores=True)
        parent_map = RankingUtil.convert_parent2rankings_to_prediction_entries(parent2rankings)
        if args.max_context_artifacts:
            parent_map = {p: c[:args.max_context_artifacts] for p, c in parent_map.items()}
        return parent_map
