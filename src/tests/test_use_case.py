from tests.base_test import BaseTest
from tests.common.request_proxy import RequestProxy
from tests.common.test_data import TestData
from tests.common.test_data_creator import TestDataCreator
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestUseCase(BaseTest):
    @mock_anthropic
    def test_use_case(self, ai_manager: TestAIManager):
        source_artifacts = TestDataCreator.get_source_artifacts()

        project_summary_json = TestData.read_summary(True)
        ai_manager.mock_project_summary(project_summary_json)
        summary_response = RequestProxy.summarize(source_artifacts)
        print(summary_response)
