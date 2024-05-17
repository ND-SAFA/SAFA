from tgen.data.keys.structure_keys import TraceKeys
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.relationship_manager.cross_encoder_manager import CrossEncoderManager
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.common.ranking_util import RankingUtil


class ReRankStep(AbstractPipelineStep[RankingArgs, RankingState]):

    def _run(self, args: RankingArgs, state: RankingState) -> None:
        """
        Re-ranks the children for each parent according using a cross-encoder.
        :param args: The ranking arguments to the pipeline.
        :param state: The state of the current pipeline.
        :return: NOne
        """
        if args.re_rank_children:
            relationship_manager = args.cross_encoder_manager if args.cross_encoder_manager \
                else CrossEncoderManager(state.artifact_map, model_name=args.ranking_model_name)
            id_pairs = [(trace[TraceKeys.SOURCE], trace[TraceKeys.TARGET]) for trace in state.selected_entries]
            scores = relationship_manager.calculate_scores(id_pairs=id_pairs)
            for trace, score in zip(state.selected_entries, scores):
                trace[TraceKeys.SCORE] = score
            child2traces = RankingUtil.group_trace_predictions(state.selected_entries, TraceKeys.child_label())
            RankingUtil.normalized_scores_by_individual_artifacts(child2traces, min_score=0)
