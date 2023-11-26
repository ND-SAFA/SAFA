from api.tests.api_base_test import APIBaseTest
from api.tests.common.mock_async import mock_async
from api.tests.common.test_data_creator import TestDataCreator
from tgen.data.keys.structure_keys import ArtifactKeys, TraceKeys
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestHGen(APIBaseTest):
    N_CLUSTERS = 2
    ARTIFACT_RESPONSES = ["Cats are cool", "Cars are stupid."]
    ARTIFACT_BODIES = ["This is a vroomy vehicle", "My motorcycle goes beep beep.", "Cats are fuzzy.", "Doggos are fluffy."]

    @mock_async
    def test_use_case(self, test_manager: TestAIManager):
        """
        Tests that user stories are able to be generated using clustering.
        """
        n_links = 4
        source_layer_id = "TypeScript"
        target_type = "User Story"

        artifacts = TestDataCreator.create_artifacts(source_layer_id, bodies=self.ARTIFACT_BODIES)

        test_manager.mock_summarization()
        for a_response in self.ARTIFACT_RESPONSES:
            test_manager.mock_hgen("user-story", [a_response])
        test_manager.mock_explanations(4)

        hgen_response = self.request("/hgen/", {"artifacts": artifacts, "targetTypes": [target_type]})
        hgen_artifacts = hgen_response["artifacts"]
        hgen_layers = hgen_response["layers"]
        hgen_links = hgen_response["links"]

        self.assertEqual(6, len(hgen_artifacts))
        generated_artifacts = [a for a in hgen_artifacts if a[ArtifactKeys.LAYER_ID.value] == target_type]
        self.assertEqual(len(self.ARTIFACT_RESPONSES), len(generated_artifacts))

        self.assertEqual(1, len(hgen_layers))
        layer_generated = hgen_layers[0]
        self.assertEqual(source_layer_id, layer_generated["child"])
        self.assertEqual(target_type, layer_generated["parent"])

        self.assertEqual(n_links, len(hgen_links))
        for t in hgen_links:
            self.assertIsNotNone(t[TraceKeys.EXPLANATION.value])
