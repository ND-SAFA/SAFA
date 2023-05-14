from api.endpoints.summary.summary_serializer import SummarizeSerializer
from api.tests.api_base_test import APIBaseTest


class TestSummarySerializer(APIBaseTest):
    """
    Tests that summary is able to be serializes
    """

    def test_pos_serialization(self):
        """
        Tests that serializer is able to parse valid payload.
        """
        chunker_type = "NL"
        artifact_id = "RE-28"
        artifact_body = "This is the body of an artifact."
        data = {
            "artifacts": {
                artifact_id: {
                    "content": artifact_body,
                    "type": chunker_type
                }
            }
        }

        serializer = SummarizeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_payload = serializer.save()
        validated_artifacts = validated_payload["artifacts"]
        self.assertEqual(1, len(validated_artifacts))
        self.assertEqual("NL", validated_artifacts[artifact_id]["type"])
