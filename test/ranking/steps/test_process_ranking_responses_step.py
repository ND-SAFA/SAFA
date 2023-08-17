from unittest import TestCase

from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.ranking.steps.step_process_ranking_responses import ProcessRankingResponses


class TestProcessRankingResponsesStep(TestCase):
    def test_process_ranked_artifacts(self):
        """
        Tests that each artifact id is processed and missing ids are added back in
        """
        parent_ids = ["parent"]
        target_ids = ["1", "2", "3", "4"]
        trace_prediction_entries = ProcessRankingResponses.process_ranked_artifacts(
            parent_ids,
            ["<explanation>"
             "0 | EXPLANATION_1 | 1\n"
             "1 | EXPLANATION_2 | 2\n"
             "2 | EXPLANATION_3 | 3\n"
             "3 | EXPLANATION_4 | 4\n"
             "</explanation>"],
            {"parent": target_ids})

        # Test children ranked correctly
        for i in range(4, 1):
            entry = trace_prediction_entries[i]
            self.assertEqual(f"{i}", entry[TraceKeys.SOURCE.value])
            self.assertEqual(f"EXPLANATION_{i + 1}", entry[TraceKeys.SOURCE.value])
