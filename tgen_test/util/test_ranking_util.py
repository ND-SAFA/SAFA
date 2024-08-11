from tgen.common.constants.metric_constants import LAG_KEY, MAP_KEY
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.keys.structure_keys import TraceKeys
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.testprojects.entry_creator import EntryCreator
from tgen.tracing.ranking.common.ranking_util import RankingUtil


class TestRankingUtil(BaseTest):
    """
    Requirements: https://www.notion.so/nd-safa/ranking_util-06b012496b7f4640be95109cdeb472f3?pvs=4
    """

    def test_evaluate_trace_predictions(self):
        """
        Be able to evaluate a set of trace predictions
        """
        true_links = EntryCreator.create_trace_predictions(3, 1, labels=[0, 1, 0])
        predictions = EntryCreator.create_trace_predictions(3, 1, scores=[0.75, 0.8, 0.95])
        trace_df = TraceDataFrame(true_links)
        metrics = RankingUtil.evaluate_trace_predictions(trace_df, predictions)
        self.assertAlmostEquals(1 / 3, metrics[MAP_KEY])  # three thresholds, AP scores are 0, 100, 0
        self.assertEqual(1, metrics[LAG_KEY])

    def test_select_predictions(self):
        """
        Be able to select the top predictions for each child
        """
        predictions = EntryCreator.create_trace_predictions(3, 1, [0.75, 0.8, 0.95])
        selected_predictions = RankingUtil.select_predictions_by_thresholds(predictions, 0.9, 0.7, 0.4)
        self.assertEqual(1, len(selected_predictions))
        prediction = selected_predictions[0]
        self.assertEqual("p2", prediction[TraceKeys.TARGET.value])
        self.assertEqual("c0", prediction[TraceKeys.SOURCE.value])

    def test_group_predictions(self):
        """
        Be able to group predictions by either parent or child.
        """
        predictions = EntryCreator.create_trace_predictions(3, 1, [0.75, 0.8, 0.95])
        grouped_predictions = RankingUtil.group_trace_predictions(predictions, TraceKeys.SOURCE.value)
        self.assertEqual(1, len(grouped_predictions))
        child_predictions = grouped_predictions["c0"]
        self.assertEqual(3, len(child_predictions))

    def test_create_parent_child_ranking(self):
        scores = [0.8, 0.5, 0.7, 0.95]
        child_ids = [str(i) for i in range(len(scores))]
        missing_id = "missing_id"
        all_child_ids = child_ids + [missing_id]
        with_scores = RankingUtil.create_parent_child_ranking(zip(child_ids, scores), set(all_child_ids), return_scores=True)
        self.assertEqual(len(with_scores), 2)
        ordered_ids, ordered_scores = with_scores
        self.assertEqual(ordered_scores[:-1], sorted(scores, reverse=True))
        for i, score in enumerate(ordered_scores[:-1]):
            expected_id = scores.index(score)
            self.assertEqual(ordered_ids[i], str(expected_id))
        self.assertEqual(ordered_ids[-1], missing_id)
        self.assertEqual(ordered_scores[-1], 0)
        without_scores = RankingUtil.create_parent_child_ranking(zip(child_ids, scores), set(all_child_ids), return_scores=False)
        self.assertEqual(ordered_ids, without_scores)
