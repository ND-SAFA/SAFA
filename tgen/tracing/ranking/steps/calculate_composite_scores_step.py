from typing import Dict, List, Tuple

from tgen.common.objects.trace import Trace
from tgen.common.util.dict_util import DictUtil
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
    def _calculate_composite_scores(parent2traces: Dict[str, List[Trace]],
                                    parent2traces_filtered: Dict[str, List[Trace]],
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
            id2chunk_scores, id2text_scores = CalculateCompositeScoreStep.extract_similarity_scores(artifact_df, traces)
            a_id2full_text_scores = {entry[TraceKeys.child_label()]: entry[TraceKeys.SCORE] for entry in parent2traces[p_id]
                                     if entry[TraceKeys.child_label()] in id2text_scores}
            # Question: are the scores different trace traces to those in parent2traces?
            parent_composite_scores = {}
            for c_id, chunk_scores in id2chunk_scores.items():
                child_scores = {CompositeScoreComponent.FULL_TEXT: a_id2full_text_scores[c_id],
                                # Question: id2text_scores is used to filters keys so isn't it the same/
                                CompositeScoreComponent.FULL_TEXT_FILTERED: id2text_scores[c_id],
                                CompositeScoreComponent.MAX_CHUNK: max(chunk_scores)}

                composite_score = CalculateCompositeScoreStep.calculate_composite_score(child_scores, chunk_scores, weights)
                parent_composite_scores[c_id] = composite_score
            composite_scores[p_id] = list(parent_composite_scores.keys()), list(parent_composite_scores.values())
        return composite_scores

    @staticmethod
    def calculate_composite_score(child_scores: Dict[CompositeScoreComponent, float],
                                  weights: Dict[CompositeScoreComponent, float],
                                  chunk_scores):
        """
        Calculates the similarity score composed of chunk score and artifact score.
        :param child_scores: Map of component to score.
        :param weights: The weights associated with each component.
        :param chunk_scores: Scores between chunk and parent.
        :return:
        """
        # No chunks selected but the full text was
        if not child_scores[CompositeScoreComponent.MAX_CHUNK] and child_scores[CompositeScoreComponent.FULL_TEXT_FILTERED]:
            child_scores[CompositeScoreComponent.MAX_CHUNK] = child_scores[CompositeScoreComponent.FULL_TEXT]
        composite_score = sum([child_scores[e] * weights.get(e, 0) for e in CompositeScoreComponent if e in child_scores])
        regular_vote = int(child_scores[CompositeScoreComponent.FULL_TEXT_FILTERED] is 0)
        votes = 1 - ((chunk_scores.count(0) + regular_vote) / (len(chunk_scores) + 1))  # number of chunks above 0
        votes = MathUtil.convert_to_new_range(votes, (0, 1),
                                              (composite_score, 1))  # scale so can only help the composite score
        composite_score += votes * weights[CompositeScoreComponent.CHUNK_VOTES]
        return composite_score

    @staticmethod
    def extract_similarity_scores(artifact_df: ArtifactDataFrame, traces: List[Trace]) -> Tuple[
        Dict[str, List[float]], Dict[str, float]]:
        """
        Extracts similarity scores, creating separate maps of scores for entities and chunks.
        :param artifact_df: The artifact data frame containing artifact's content.
        :param traces: The traces to calculate similarity scores for.
        :return: Map of chunk scores, Map of full text scores.
        """
        id2chunk_scores: Dict[str, List[float]] = {}
        id2text_scores: Dict[str, float] = {}
        for trace in traces:
            c_id, score = trace[TraceKeys.child_label()], trace[TraceKeys.SCORE]
            orig_id = artifact_df.get_orig_id(c_id)
            if orig_id == c_id:
                id2text_scores[orig_id] = score
            else:
                DictUtil.set_or_append_item(id2chunk_scores, orig_id, score)
        return id2chunk_scores, id2text_scores
