from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.tracing.ranking.ranking_args import RankingArgs
from tgen.tracing.ranking.ranking_state import RankingState


class FilterLinksBelowThresholdStep(AbstractPipelineStep[RankingArgs, RankingState]):

    def _run(self, args: RankingArgs, state: RankingState) -> None:
        """
        Filters out links that are below the threshold
        :param args: The arguments to the ranking pipeline
        :param state: The current state of the ranking pipeline
        """
        if not state.children_entries:
            state.children_entries = [entry for entries in state.sorted_parent2children.values() for entry in entries]
        state.selected_entries = [c for c in state.children_entries if TraceKeys.SCORE in c and
                                  c[TraceKeys.SCORE] >= args.link_threshold]
