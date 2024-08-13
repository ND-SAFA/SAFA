from copy import deepcopy
from unittest import TestCase

from tgen_test.ranking.steps.ranking_pipeline_test import DEFAULT_PARENT_IDS, DEFAULT_CHILDREN_IDS, RankingPipelineTest
from tgen.common.constants.ranking_constants import RANKING_MAX_SCORE, RANKING_MIN_SCORE
from common_resources.tools.util.math_util import MathUtil
from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.keys.structure_keys import TraceKeys
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.steps.process_ranking_responses_step import ProcessRankingResponsesStep


class TestProcessRankingResponsesStep(TestCase):

    def test_run(self):
        embedding_score = 0.35
        parent_ids = DEFAULT_PARENT_IDS
        children_ids = DEFAULT_CHILDREN_IDS
        scores = [[1.0, 2.0], [2.0, 1.0]]
        args = RankingArgs(parent_ids=parent_ids, children_ids=children_ids, dataset=PromptDataset(artifact_df=ArtifactDataFrame()),
                           weight_of_embedding_scores=0, weight_of_explanation_scores=0, types_to_trace=("target", "source"))
        ranking_responses = [[{'id': [0], 'score': [scores[0][0]]},
                              {'id': [], 'score': [scores[0][1]]}], [
                                 {'id': [1], 'score': [scores[1][1]]}]]
        missing = (parent_ids[1], children_ids[0])
        for res in ranking_responses:
            for r in res:
                r.update({tag: tag.upper() for tag in RankingPipelineTest.get_explanation_tags()})
        state = RankingState(sorted_parent2children={p_id: [RankingUtil.create_entry(p_id, c_id, score=embedding_score)
                                                            for c_id in children_ids]
                                                     for p_id in parent_ids},
                             ranking_responses=ranking_responses)

        ProcessRankingResponsesStep().run(args, state)
        expected = {p_id: deepcopy(children_ids) for p_id in parent_ids}
        found = {p_id: [] for p_id in parent_ids}
        for entry in state.candidate_entries:
            c_id = entry[TraceKeys.SOURCE.value]
            c_index = children_ids.index(c_id)
            p_id = entry[TraceKeys.TARGET.value]
            p_index = parent_ids.index(p_id)
            score = entry[TraceKeys.SCORE.value]
            expected_score = MathUtil.normalize_val(scores[p_index][c_index],
                                                    max_val=RANKING_MAX_SCORE, min_val=RANKING_MIN_SCORE)
            if p_id == missing[0] and c_id == missing[1]:
                expected_score = embedding_score
            self.assertEqual(score, expected_score)
            found[p_id].append(c_id)
        for p_id in found.keys():
            self.assertEqual(len(found[p_id]), len(expected[p_id]))
            for c_id in expected[p_id]:
                self.assertIn(c_id, found[p_id])
