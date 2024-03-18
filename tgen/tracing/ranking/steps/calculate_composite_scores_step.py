from typing import Dict, List, Tuple

from tgen.common.util.dict_util import DictUtil
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.math_util import MathUtil
from tgen.common.util.supported_enum import SupportedEnum
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import TraceKeys
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.common.ranking_util import RankingUtil


class CompositeScoreComponent(SupportedEnum):
    FULL_TEXT = 0
    MAX_CHUNK = 1
    CHUNK_VOTES = 2
    FULL_TEXT_FILTERED = 3


class CalculateCompositeScoreStep(AbstractPipelineStep[RankingArgs, RankingState]):
    WEIGHTS = {CompositeScoreComponent.FULL_TEXT: 0.4, CompositeScoreComponent.MAX_CHUNK: 0.4,
               CompositeScoreComponent.CHUNK_VOTES: 0.2}

    def _run(self, args: RankingArgs, state: RankingState) -> None:
        """
        Sorts the children + chunks for each parent according and combines their scores.
        :param args: The ranking arguments to the pipeline.
        :param state: The state of the current pipeline.
        :return: None.
        """
        if not args.use_chunks:
            return

        parent_map = state.get_current_parent2children()
        composite_scores = self._calculate_composite_scores(state.sorted_parent2children,
                                                            parent_map, args.dataset.artifact_df, self.WEIGHTS)
        state.composite_parent2children = RankingUtil.convert_parent2rankings_to_prediction_entries(composite_scores)

    @staticmethod
    def _calculate_composite_scores(parent2traces: Dict[str, List[EnumDict]],
                                    parent2traces_filtered: Dict[str, List[EnumDict]],
                                    artifact_df: ArtifactDataFrame,
                                    weights: Dict[CompositeScoreComponent, float]) -> Dict[str, Tuple[List, List]]:
        """
        Calculates the composite score across all chunks and the full text.
        :param parent2traces_filtered: Maps parent id to a list of traces (including chunks).
        :param artifact_df: Contains all original artifacts in the dataset.
        :param weights: Map of composite score component to the weight for each of the scores.
        :return: A dictionary mapping parent to its children and their composite score.
        """
        composite_scores = {}
        for p_id, traces in parent2traces_filtered.items():
            a_id2chunk_scores: Dict[str, List[float]] = {}
            a_id2full_text_scores_filtered: Dict[str, float] = {}
            for trace in traces:
                c_id, score = trace[TraceKeys.child_label()], trace[TraceKeys.SCORE]
                orig_id = artifact_df.get_orig_id(c_id)
                if orig_id == c_id:
                    a_id2full_text_scores_filtered[orig_id] = score
                else:
                    DictUtil.set_or_append_item(a_id2chunk_scores, orig_id, score)
            a_id2full_text_scores = {entry[TraceKeys.child_label()]: entry[TraceKeys.SCORE] for entry in parent2traces[p_id]
                                     if entry[TraceKeys.child_label()] in a_id2full_text_scores_filtered}
            parent_composite_scores = {}
            for c_id, chunk_scores in a_id2chunk_scores.items():
                child_scores = {CompositeScoreComponent.FULL_TEXT: a_id2full_text_scores[c_id],
                                CompositeScoreComponent.FULL_TEXT_FILTERED: a_id2full_text_scores_filtered[c_id],
                                CompositeScoreComponent.MAX_CHUNK: max(chunk_scores)}

                # No chunks selected but the full text was
                if not child_scores[CompositeScoreComponent.MAX_CHUNK] and child_scores[CompositeScoreComponent.FULL_TEXT_FILTERED]:
                    child_scores[CompositeScoreComponent.MAX_CHUNK] = child_scores[CompositeScoreComponent.FULL_TEXT]
                composite_score = sum([child_scores[e] * weights.get(e, 0) for e in CompositeScoreComponent if e in child_scores])

                regular_vote = int(child_scores[CompositeScoreComponent.FULL_TEXT_FILTERED] is 0)
                votes = 1 - ((chunk_scores.count(0) + regular_vote) / (len(chunk_scores) + 1))  # number of chunks above 0
                votes = MathUtil.convert_to_new_range(votes, (0, 1),
                                                      (composite_score, 1))  # scale so can only help the composite score

                parent_composite_scores[c_id] = composite_score + votes * weights[CompositeScoreComponent.CHUNK_VOTES]
            composite_scores[p_id] = list(parent_composite_scores.keys()), list(parent_composite_scores.values())
        return composite_scores
