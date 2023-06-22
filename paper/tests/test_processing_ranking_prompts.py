from unittest import TestCase

from paper.pipeline.response_process_step import process_ranked_artifacts
from tgen.models.llm.llm_responses import GenerationResponse


class TestProcessingRankingPrompts(TestCase):
    def test_basic(self):
        """
        Tests that each artifact id is processed and missing ids are added back in
        """
        batch_response = GenerationResponse(["1,2.java,3.xml", "2,  3,4"])
        target_ids = ["1", "2", "3", "4"]
        processed_response = process_ranked_artifacts(batch_response, target_ids)

        self.assertEqual(2, len(processed_response))
        self.assertEqual("1", processed_response[0][0])
        self.assertEqual("2", processed_response[0][1])
        self.assertEqual("3", processed_response[0][2])
        self.assertEqual("4", processed_response[0][3])

        self.assertEqual("2", processed_response[1][0])
        self.assertEqual("3", processed_response[1][1])
        self.assertEqual("4", processed_response[1][2])
        self.assertEqual("1", processed_response[1][3])
