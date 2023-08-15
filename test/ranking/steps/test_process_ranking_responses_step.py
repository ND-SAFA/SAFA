from unittest import TestCase

from tgen.ranking.steps.step_process_ranking_responses import ProcessRankingResponses


class TestProcessRankingResponsesStep(TestCase):
    def test_process_ranked_artifacts(self):
        """
        Tests that each artifact id is processed and missing ids are added back in
        """
        parent_ids = ["parent"]
        target_ids = ["1", "2", "3", "4"]
        ranked_children_global, children_explanations_global = ProcessRankingResponses.process_ranked_artifacts(
            parent_ids,
            ["<explanation>"
             "0 | SUMMARY | EXPLANATION_1 | 1\n"
             "1 | SUMMARY | EXPLANATION_2 | 2\n"
             "2 | SUMMARY | EXPLANATION_3 | 3\n"
             "3 | SUMMARY | EXPLANATION_4 | 4\n"
             "</explanation>"],
            {"parent": target_ids})

        # Test children ranked correctly
        ranked_children = ranked_children_global[0]
        self.assertEqual("4", ranked_children[0])
        self.assertEqual("3", ranked_children[1])
        self.assertEqual("2", ranked_children[2])
        self.assertEqual("1", ranked_children[3])

        # Test explanations parsed correctly
        children_explanations = children_explanations_global[0]
        self.assertEqual("EXPLANATION_4", children_explanations[0])
        self.assertEqual("EXPLANATION_3", children_explanations[1])
        self.assertEqual("EXPLANATION_2", children_explanations[2])
        self.assertEqual("EXPLANATION_1", children_explanations[3])
