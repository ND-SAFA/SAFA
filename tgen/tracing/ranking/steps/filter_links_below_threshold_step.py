from tgen.common.util.logging.logger_manager import logger
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.common.selection_methods import SupportedSelectionMethod


class FilterLinksBelowThresholdStep(AbstractPipelineStep[RankingArgs, RankingState]):

    def _run(self, args: RankingArgs, state: RankingState) -> None:
        """
        Filters out links that are below the threshold
        :param args: The arguments to the ranking pipeline
        :param state: The current state of the ranking pipeline
        """
        if not state.children_entries:
            state.children_entries = [entry for entries in state.sorted_parent2children.values() for entry in entries]
        if args.selection_method == SupportedSelectionMethod.FILTER_BY_THRESHOLD:
            logger.info(f"Selecting links with scores above {args.link_threshold}")
            state.selected_entries = [c for c in state.children_entries if TraceKeys.SCORE in c and
                                      c[TraceKeys.SCORE] >= args.link_threshold]
        elif args.selection_method == SupportedSelectionMethod.SELECT_TOP_PARENTS:
            logger.info(f"Selecting top parents for each child artifact")
            state.selected_entries = RankingUtil.select_predictions(state.children_entries)
        else:
            logger.info(f"Keeping all links for evaluation.")
            state.selected_entries = state.children_entries
