from typing import Dict, List

from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.tracing.ranking.sorters.supported_sorters import SupportedSorter
from tgen.tracing.ranking.ranking_args import RankingArgs
from tgen.tracing.ranking.ranking_state import RankingState


class SortChildren(AbstractPipelineStep[RankingArgs, RankingState]):

    def _run(self, args: RankingArgs, state: RankingState) -> None:
        """
        Sorts the children for each parent according to specified sorting function.
        :param args: The ranking arguments to the pipeline.
        :param state: The state of the current pipeline.
        :return: NOne
        """
        use_sorter = args.sorter is not None
        use_pre_ranked = args.parent2children is not None

        if use_pre_ranked:
            n_parents = len(args.parent_ids)
            n_children = len(args.children_ids)
            state.sorted_parent2children = args.parent2children
            add_sorted_children = len(args.parent2children) < n_parents or any(
                [len(v) < n_children for v in args.parent2children.values()])
            if add_sorted_children:
                state.sorted_parent2children = self.add_missing_children(args)
        elif use_sorter:
            parent_map = self.create_sorted_parent_map(args)
            state.sorted_parent2children = parent_map
        else:
            raise AssertionError("Expected sorter or parent2children to be defined.")

    @staticmethod
    def add_missing_children(args) -> Dict[str, List[str]]:
        """
        Adds any children missing in args.parent2children in the order defined by sorter.
        :param args: The ranking pipeline arguments.
        :return: None (modified in place)
        """
        original_max_content = args.max_context_artifacts
        args.max_context_artifacts = None
        sorted_parent_map = SortChildren.create_sorted_parent_map(args)
        final_parent_map = {}
        for p, sorted_children in sorted_parent_map.items():
            defined_children = args.parent2children.get(p, [])
            defined_children_set = set(defined_children)
            missing_children = [c for c in sorted_children if c not in defined_children_set]
            final_parent_map[p] = defined_children + missing_children
        args.max_context_artifacts = original_max_content
        return final_parent_map

    @staticmethod
    def create_sorted_parent_map(args):
        """
        Sorts the children artifacts against each parent, resulting in a list of children from most to least similar.
        :param args: The ranking pipeline arguments.
        :return: The map of parent IDs to sorted children IDs.
        """
        sorting_function = SupportedSorter.get_value(args.sorter.upper())
        parent_map = sorting_function(args.parent_ids, args.children_ids, args.artifact_map, model_name=args.embedding_model)
        parent_map = {p: c[:args.max_context_artifacts] for p, c in parent_map.items()}
        return parent_map
