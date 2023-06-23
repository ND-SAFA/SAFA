from unittest import TestCase

from paper.pipeline.map_step import process_artifact_ids, process_response


class TestProcessingSteps(TestCase):
    def test_response_processing(self):
        response = process_response("ID: 1, ID: 2")
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0], " 1")
        self.assertEqual(response[1], "  2")

    def test_id_parsing(self):
        response = process_artifact_ids(["1", "2.java"])
        self.assertEqual(response[0], "1")
        self.assertEqual(response[1], "2")
