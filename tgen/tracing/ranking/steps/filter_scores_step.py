from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState


class FilterScoresStep(AbstractPipelineStep[RankingArgs, RankingState]):

    def _run(self, args: RankingArgs, state: RankingState) -> None:
        """
        Filters the children for each parent according to specified filter function. Filtered children will have a score of 0.
        :param args: The ranking arguments to the pipeline.
        :param state: The state of the current pipeline.
        :return: None
        """
        if args.filter:
            state.filtered_parent2children = args.filter.value.filter(state.get_current_parent2children(),
                                                                      args.children_ids, args.parent_ids)
