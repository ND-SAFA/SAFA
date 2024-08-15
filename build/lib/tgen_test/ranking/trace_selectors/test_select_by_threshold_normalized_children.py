from unittest import TestCase

from common_resources.tools.util.enum_util import EnumDict
from common_resources.data.keys.structure_keys import TraceKeys
from tgen.tracing.ranking.common.ranking_util import RankingUtil


class TestSelectByThresholdNormalizedChildren(TestCase):

    def test_select(self):
        children_entries = [EnumDict({'id': 1, 'source': 't6', 'target': 's4', 'score': 0.4}),
                            EnumDict({'id': 2, 'source': 't1', 'target': 's4', 'score': 0.7}),
                            EnumDict({'id': 3, 'source': 't2', 'target': 's4', 'score': 0.5}),
                            EnumDict({'id': 4, 'source': 't6', 'target': 's5', 'score': 0.5}),
                            EnumDict({'id': 5, 'source': 't1', 'target': 's5', 'score': 0.7}),
                            EnumDict({'id': 6, 'source': 't2', 'target': 's5', 'score': 0.2})
                            ]
        parent2children = RankingUtil.group_trace_predictions(predictions=children_entries,
                                                              key_id=TraceKeys.parent_label())
        parent2scores = {p_id: [trace[TraceKeys.SCORE] for trace in traces] for p_id, traces in parent2children.items()}
        self.assertIn("s4", parent2children)
        self.assertEqual(parent2children["s4"], children_entries[:3])
        self.assertEqual(parent2scores["s4"], [entry['score'] for entry in children_entries[:3]])
        self.assertIn("s5", parent2children)
        self.assertEqual(parent2children["s5"], children_entries[3:])
        self.assertEqual(parent2scores["s5"], [entry['score'] for entry in children_entries[3:]])
        RankingUtil.normalized_scores_by_individual_artifacts(parent2children)
        RankingUtil.select_traces_by_artifact(parent2children, threshold=0.8)
        top_scores_indices = [1, 4]
        low_scores_indices = [0, 5]
        for i in top_scores_indices:
            self.assertEqual(children_entries[i]['score'], 1)
        for i in low_scores_indices:
            self.assertEqual(children_entries[i]['score'], 0)
        mid_score1 = children_entries[2]['score']
        self.assertLess(mid_score1 - 0, 1 - mid_score1)  # score is closer to lower score than upper
        mid_score2 = children_entries[3]['score']
        self.assertGreater(mid_score2 - 0, 1 - mid_score2)  # score is closer to upper score than lower
