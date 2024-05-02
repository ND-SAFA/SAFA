from test.contradictions.data_test_requirements import R1, get_response_for_req, get_artifact_content
from tgen.common.objects.artifact import Artifact
from tgen.contradictions.requirements_converter import RequirementsConverter
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestRequirementsConverter(BaseTest):

    @mock_anthropic
    def test_convert_artifacts(self, test_ai_manager: TestAIManager):
        artifact_content = get_artifact_content(R1)
        artifact = Artifact(id="1", content=artifact_content, layer_id="requirement")
        response = get_response_for_req(R1)
        test_ai_manager.set_responses([response])
        requirements = RequirementsConverter().convert_artifacts([artifact])
        self.assertDictEqual(vars(R1), vars(requirements[0]))
