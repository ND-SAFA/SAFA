from unittest import TestCase

from api.endpoints.summary.summary_serializer import SummarySerializer


class TestSummarySerializer(TestCase):
    """
    Tests that summary is able to be serializes
    """

    def test_pos_serialization(self):
        """
        Tests that serializer is able to parse valid payload.
        """
        data = {
            "artifacts": {
                "RE-28": "This is the body of an artifact."
            }
        }

        serializer = SummarySerializer(data=data)
        self.assertTrue(serializer.is_valid())
