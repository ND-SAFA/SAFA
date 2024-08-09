from unittest import TestCase

from tgen_test.ranking.steps.ranking_pipeline_test import RankingPipelineTest
from tgen.common.objects.chunk import Chunk
from tgen.common.objects.trace import Trace
from tgen.data.keys.structure_keys import TraceKeys
from tgen.tracing.ranking.steps.calculate_composite_scores_step import CalculateCompositeScoreStep


class TestCompositeScoreStep(TestCase):

    def test_run(self):
        args, state = RankingPipelineTest.create_ranking_structures()
        args.use_chunks = True
        args.parent_ids = args.parent_ids[:2]
        args.children_ids = args.children_ids[:1]
        full_text_score = 0.5

        scores = [[full_text_score, 0.5, 0.6, 0.7], [full_text_score, 0.4, 0.4, 0.4]]
        filtered = [[False, True, False, False], [False, True, True, True]]
        chunks = [Chunk.get_chunk_id(args.children_ids[0], i) for i in range(len(scores[0]) - 1)]
        all_children_ids = args.children_ids[:1] + chunks
        state.sorted_parent2children = {
            p_id: [Trace(target=p_id, source=c_id, score=scores[i][j]) for j, c_id in enumerate(all_children_ids)]
            for i, p_id in enumerate(args.parent_ids)}
        state.filtered_parent2children = {p_id: [Trace(target=p_id, source=c_id,
                                                       score=state.sorted_parent2children[p_id][j][TraceKeys.SCORE] if not filtered[i][
                                                           j] else 0)
                                                 for j, c_id in enumerate(all_children_ids)]
                                          for i, p_id in enumerate(args.parent_ids)}

        c_id = all_children_ids[0]
        for i, p_id in enumerate(args.parent_ids):
            a_id2full_text_scores_filtered, a_id2chunk_scores = CalculateCompositeScoreStep._group_scores_by_full_or_chunk(
                traces=state.filtered_parent2children[p_id],
                artifact_df=args.dataset.artifact_df)
            self.assertEqual(a_id2full_text_scores_filtered[c_id], full_text_score)
            self.assertListEqual(a_id2chunk_scores[c_id], [score if not filtered[i][j + 1] else 0
                                                           for j, score in enumerate(scores[i][1:])])
            child_scores = CalculateCompositeScoreStep._get_scores_for_child(c_id, a_id2full_text_scores_filtered,
                                                                             a_id2chunk_scores, full_text_score)
            composite_score = CalculateCompositeScoreStep._calculate_composite_score(child_scores, CalculateCompositeScoreStep.WEIGHTS)
            combined_score_sum = max(scores[i][1:]) + full_text_score if i == 0 else 2 * full_text_score
            self.assertEqual(composite_score, ((combined_score_sum / 2) * 0.8))
            votes = CalculateCompositeScoreStep._tally_votes(child_scores, a_id2chunk_scores.get(c_id, [full_text_score]), True)
            self.assertEqual(votes, (sum([int(not filtered) for filtered in filtered[i]]) / len(filtered[i])))
