from typing import Dict, List, Tuple

from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.keys.structure_keys import TraceKeys
from gen_common.data.objects.trace import Trace
from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep
from gen_common.traceability.ranking.common.ranking_args import RankingArgs
from gen_common.traceability.ranking.common.ranking_state import RankingState
from gen_common.util.dict_util import DictUtil
from gen_common.util.enum_util import EnumDict
from gen_common.util.math_util import MathUtil
from gen_common.util.ranking_util import RankingUtil
from gen_common.util.supported_enum import SupportedEnum


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
            a_id2full_text_scores_filtered, a_id2chunk_scores = CalculateCompositeScoreStep._group_scores_by_full_or_chunk(traces,
                                                                                                                           artifact_df)
            a_id2full_text_scores = {entry[TraceKeys.child_label()]: entry[TraceKeys.SCORE] for entry in parent2traces[p_id]
                                     if entry[TraceKeys.child_label()] in a_id2full_text_scores_filtered}
            parent_composite_scores = {}
            for c_id, full_text_score in a_id2full_text_scores.items():
                has_chunks = c_id in a_id2chunk_scores
                all_chunk_scores = a_id2chunk_scores.get(c_id, [full_text_score])
                child_scores = CalculateCompositeScoreStep._get_scores_for_child(c_id, a_id2full_text_scores_filtered,
                                                                                 a_id2chunk_scores, full_text_score)

                composite_score = CalculateCompositeScoreStep._calculate_composite_score(child_scores, weights)
                votes = CalculateCompositeScoreStep._tally_votes(child_scores, all_chunk_scores, has_chunks)
                votes = MathUtil.convert_to_new_range(votes, (0, 1), (composite_score, 1))  # scale so only helps the composite score
                parent_composite_scores[c_id] = composite_score + votes * weights[CompositeScoreComponent.CHUNK_VOTES]  # add votes
            composite_scores[p_id] = list(parent_composite_scores.keys()), list(parent_composite_scores.values())
        return composite_scores

    @staticmethod
    def _get_scores_for_child(c_id: str, a_id2full_text_scores_filtered: Dict[str, float], a_id2chunk_scores: Dict[str, List[float]],
                              full_text_score) -> Dict[CompositeScoreComponent, float]:
        """
        Maps each composite score component (e.g. full text and chunk scores) to the score assigned to it.
        :param c_id: The child id.
        :param a_id2full_text_scores_filtered: Maps the artifact id to the full text score with filtering.
        :param a_id2chunk_scores: Maps the artifact id to the full chunk scores with filtering.
        :param full_text_score: Maps the artifact id to the original full text score.
        :return: Dictionary mapping each composite score component to the score assigned to it.
        """
        child_scores = {CompositeScoreComponent.FULL_TEXT: full_text_score,
                        CompositeScoreComponent.FULL_TEXT_FILTERED: a_id2full_text_scores_filtered[c_id],
                        CompositeScoreComponent.MAX_CHUNK: max(a_id2chunk_scores.get(c_id, [full_text_score]))}
        return child_scores

    @staticmethod
    def _calculate_composite_score(child_scores: Dict[CompositeScoreComponent, float],
                                   weights: Dict[CompositeScoreComponent, float]) -> float:
        """
        Calculates the composite score using the given weights and Maps each composite score component to the score assigned to it..
        :param child_scores: Maps each composite score component to the score assigned to it.
        :param weights: Maps each composite score component to the weight assigned to it.
        :return: The composite score using the given weights and full text and chunk scores.
        """
        if not child_scores[CompositeScoreComponent.MAX_CHUNK] and child_scores[CompositeScoreComponent.FULL_TEXT_FILTERED]:
            # No chunks selected but the full text was
            child_scores[CompositeScoreComponent.MAX_CHUNK] = child_scores[CompositeScoreComponent.FULL_TEXT]
        composite_score = sum([child_scores[e] * weights.get(e, 0) for e in CompositeScoreComponent if e in child_scores])
        return composite_score

    @staticmethod
    def _tally_votes(child_scores: Dict[CompositeScoreComponent, float], all_chunk_scores: List[float], has_chunks: bool) -> float:
        """
        Calculates the composite score using the given weights and full text and chunk scores.
        :param child_scores: Maps each composite score component to the score assigned to it.
        :param all_chunk_scores: List of scores for each chunk.
        :param has_chunks: If True, the current artifact being examined has at least one chunk.
        """
        regular_vote = int(child_scores[CompositeScoreComponent.FULL_TEXT_FILTERED] is 0)
        if has_chunks:
            votes = 1 - ((all_chunk_scores.count(0) + regular_vote) / (len(all_chunk_scores) + 1))  # number of chunks above 0

        else:
            votes = 1 - regular_vote  # no chunks so only use regular text
        return votes

    @staticmethod
    def _group_scores_by_full_or_chunk(traces: List[Trace],
                                       artifact_df: ArtifactDataFrame) -> Tuple[Dict[str, float], Dict[str, List[float]]]:
        """
        Groups all traces as either having a child that is a full text artifact or a chunk of an artifact.
        :param traces: List of all traces.
        :param artifact_df: The artifact dataframe containing all artifacts.
        :return: A dictionary mapping artifact id to the full text score and one mapping artifact id to a list of chunk scores.sta
        """
        a_id2chunk_scores: Dict[str, List[float]] = {}
        a_id2full_text_scores_filtered: Dict[str, float] = {}
        for trace in traces:
            c_id, score = trace[TraceKeys.child_label()], trace[TraceKeys.SCORE]
            orig_id = artifact_df.get_artifact_from_chunk_id(c_id, id_only=True)
            if orig_id == c_id:
                a_id2full_text_scores_filtered[orig_id] = score
            else:
                DictUtil.set_or_append_item(a_id2chunk_scores, orig_id, score)
        return a_id2full_text_scores_filtered, a_id2chunk_scores
