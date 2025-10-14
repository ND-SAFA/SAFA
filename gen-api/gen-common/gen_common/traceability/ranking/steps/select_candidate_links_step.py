from gen_common.infra.t_logging.logger_manager import logger
from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep
from gen_common.traceability.ranking.common.ranking_args import RankingArgs
from gen_common.traceability.ranking.common.ranking_state import RankingState
from gen_common.traceability.ranking.trace_selectors.i_selection_method import iSelector


class SelectCandidateLinksStep(AbstractPipelineStep[RankingArgs, RankingState]):

    def _run(self, args: RankingArgs, state: RankingState) -> None:
        """
        Filters out links that are below the threshold
        :param args: The arguments to the ranking pipeline
        :param state: The current state of the ranking pipeline
        """
        candidate_entries = state.get_current_entries()
        if args.selection_method is not None:
            selection_method: iSelector = args.selection_method.value
            state.selected_entries = selection_method.select(candidate_entries,
                                                             threshold=args.link_threshold,
                                                             parent_thresholds=args.parent_thresholds)
            logger.info(f"Found {len(state.selected_entries)} links matching criteria.")
        if not state.selected_entries:
            logger.info(f"Keeping all links ({len(candidate_entries)}).")
            state.selected_entries = candidate_entries
