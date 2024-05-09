from api.endpoints.gen.summarize.summarize_serializer import SummarizeRequest, SummarizeSerializer
from apiTests.base_test import BaseTest
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys


class TestSummarySerializer(BaseTest):
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
            "artifacts": [
                {
                    "id": artifact_id,
                    "content": artifact_body,
                    "layer_id": chunker_type
                }
            ]
        }

        serializer = SummarizeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_payload: SummarizeRequest = serializer.save()
        validated_artifacts = validated_payload.artifacts
        self.assertEqual(1, len(validated_artifacts))
        artifact = validated_artifacts[0]
        self.assertEqual(chunker_type, artifact[ArtifactKeys.LAYER_ID.value])
        self.assertEqual(artifact_body, artifact[ArtifactKeys.CONTENT.value])
        self.assertEqual(artifact_id, artifact[ArtifactKeys.ID.value])
