from typing import Dict, List

from tgen.common.util.enum_util import EnumDict
from tgen.data.keys.structure_keys import TraceKeys
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep
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
        use_sorter = args.sorter is not None
        use_pre_ranked = args.pre_sorted_parent2children is not None

        if use_pre_ranked:
            n_parents = len(args.parent_ids)
            n_children = len(args.children_ids)
            parent2rankings = args.pre_sorted_parent2children
            state.sorted_parent2children = {p: [RankingUtil.create_entry(p, c) for c in rankings] for p, rankings in
                                            parent2rankings.items()}
            add_sorted_children = len(args.pre_sorted_parent2children) < n_parents or any(
                [len(v) < n_children for v in args.pre_sorted_parent2children.values()])
            if add_sorted_children:
                state.sorted_parent2children = self.add_missing_children(args, state)
        elif use_sorter:
            parent_map = self.create_sorted_parent_map(args, state)
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
    def create_sorted_parent_map(args: RankingArgs, state: RankingState) -> Dict[str, List]:
        """
        Sorts the children artifacts against each parent, resulting in a list of children from most to least similar.
        :param args: The ranking pipeline arguments.
        :param state: The current state of the ranking pipeline
        :return: The map of parent IDs to sorted children IDs.
        """
        sorter: iSorter = SupportedSorter.get_value(args.sorter.upper())
        parent2rankings = sorter.sort(args.parent_ids, args.children_ids, state.artifact_map,
                                      model_name=args.embedding_model_name, return_scores=True)
        parent_map = RankingUtil.convert_parent2rankings_to_prediction_entries(parent2rankings)
        parent_map = {p: c[:args.max_context_artifacts] for p, c in parent_map.items()}
        return parent_map
