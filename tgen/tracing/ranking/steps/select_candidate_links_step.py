from tgen.common.util.logging.logger_manager import logger
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.common.selection_methods import SupportedSelectionMethod


class SelectCandidateLinksStep(AbstractPipelineStep[RankingArgs, RankingState]):

    def _run(self, args: RankingArgs, state: RankingState) -> None:
        """
        Filters out links that are below the threshold
        :param args: The arguments to the ranking pipeline
        :param state: The current state of the ranking pipeline
        """
        candidate_entries = state.get_current_entries()
        if args.selection_method == SupportedSelectionMethod.FILTER_BY_THRESHOLD:
            logger.info(f"Selecting links with scores above {args.link_threshold}.")
            state.selected_entries = [c for c in candidate_entries if TraceKeys.SCORE in c and
                                      c[TraceKeys.SCORE] >= args.link_threshold]
        elif args.selection_method == SupportedSelectionMethod.SELECT_TOP_PARENTS:
            logger.info(f"Selecting top parents for each child artifact.")
            state.selected_entries = RankingUtil.select_predictions(candidate_entries)
        if args.selection_method is not None:
            logger.info(f"Found {len(state.selected_entries)} links matching criteria.")
        if not state.selected_entries:
            logger.info(f"Keeping all links.")
            state.selected_entries = candidate_entries


