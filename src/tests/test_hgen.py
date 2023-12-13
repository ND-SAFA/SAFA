from tests.base_test import BaseTest
from tests.common.request_proxy import RequestProxy
from tests.common.test_constants import CHILD_TYPE, PARENT_TYPE
from tests.common.test_data import TestArtifacts, TestData
from tgen.common.objects.artifact import Artifact
from tgen.data.keys.structure_keys import ArtifactKeys, TraceKeys
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestHGen(BaseTest):
    N_CLUSTERS = 2
    ARTIFACT_RESPONSES = ["Cats are cool", "Cars are stupid."]
    ARTIFACT_BODIES = ["This is a vroomy vehicle", "My motorcycle goes beep beep.", "Cats are fuzzy.", "Doggos are fluffy."]

    @mock_anthropic
    def test_use_case(self, test_manager: TestAIManager):
        """
        Tests that user stories are able to be generated using clustering.
        """
        n_links = 5
        source_layer_id = CHILD_TYPE
        target_type = PARENT_TYPE

        source_artifacts = TestData.read_artifacts(TestArtifacts.CHILD)
        target_artifacts = TestData.read_artifacts(TestArtifacts.PARENT)
        target_artifacts.reverse()

        generation_xml_map = {"functional-requirement": [a[ArtifactKeys.CONTENT] for a in target_artifacts]}
        title_xml_map = {"title": [a[ArtifactKeys.ID] for a in target_artifacts]}

        test_manager.add_xml_response(generation_xml_map, as_single_res=True)
        test_manager.add_xml_response(title_xml_map)

        test_manager.mock_explanations(n_links)

        hgen_response = RequestProxy.hgen(source_artifacts, target_type, summary=TestData.read_summary())
        assert isinstance(hgen_response, dict), f"{hgen_response}"
        hgen_artifacts = [Artifact(**a) for a in hgen_response["artifacts"]]
        hgen_layers = hgen_response["layers"]
        hgen_links = hgen_response["links"]

        self.assertEqual(len(source_artifacts) + len(target_artifacts), len(hgen_artifacts))
        for t in target_artifacts:
            t_id = t[ArtifactKeys.ID]
            artifact_query = [a for a in hgen_artifacts if f"] {t_id}" in a[ArtifactKeys.ID]]
            assert len(artifact_query) == 1, f"Expected {artifact_query} to contain single item."
            generated_artifact = artifact_query[0]
            self.assertEqual(generated_artifact[ArtifactKeys.CONTENT], t[ArtifactKeys.CONTENT])

        self.assertEqual(1, len(hgen_layers))
        layer_generated = hgen_layers[0]
        self.assertEqual(source_layer_id, layer_generated["child"])
        self.assertEqual(target_type, layer_generated["parent"])

        self.assertEqual(n_links, len(hgen_links))
        for t in hgen_links:
            self.assertIsNotNone(t[TraceKeys.EXPLANATION.value])
