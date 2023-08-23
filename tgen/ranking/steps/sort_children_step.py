from tgen.ranking.common.vsm_sorter import registered_sorters
from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_state import RankingState
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


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
        if use_sorter and use_pre_ranked:
            raise AssertionError("Please provide sorter or parent2children, but not both.")

        if use_sorter:
            sorting_function = registered_sorters[args.sorter.lower()]
            parent_map = sorting_function(args.parent_ids, args.children_ids, args.artifact_map, model_name=args.embedding_model)
            parent_map = {p: c[:args.max_context_artifacts] for p, c in parent_map.items()}
            state.sorted_parent2children = parent_map
        elif use_pre_ranked:
            state.sorted_parent2children = args.parent2children
        else:
            raise AssertionError("Expected sorter or parent2children to be defined.")
