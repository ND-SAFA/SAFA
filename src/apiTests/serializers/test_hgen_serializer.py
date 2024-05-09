from api.endpoints.gen.hgen.hgen_serializer import HGenRequest, HGenSerializer
from apiTests.base_test import BaseTest
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.testres.test_assertions import TestAssertions


class TestHGenSerializer(BaseTest):
    data = {
        "artifacts": [{
            "id": "A1",
            "content": "This is the content of the artifact.",
            "layer_id": "A"
        }],
        "targetTypes": ["user story", "epic"]
    }

    def test_positive_serialization(self):
        hgen_serializer = HGenSerializer(data=self.data)
        hgen_serializer.is_valid(raise_exception=True)
        hgen_request: HGenRequest = hgen_serializer.save()

        artifact_df = ArtifactDataFrame(hgen_request.artifacts)
        TestAssertions.verify_entities_in_df(self, self.data["artifacts"], artifact_df)

        target_types = hgen_request.target_types
        self.assertEqual(2, len(target_types))
        for t_type in self.data["targetTypes"]:
            self.assertIn(t_type, target_types)
