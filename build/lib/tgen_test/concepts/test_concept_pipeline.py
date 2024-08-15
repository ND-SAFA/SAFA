from common_resources.mocking.mock_anthropic import mock_anthropic
from common_resources.mocking.test_response_manager import TestAIManager

from tgen.concepts.concept_pipeline import ConceptPipeline
from tgen.testres.base_tests.base_test import BaseTest
from tgen_test.concepts.test_create_response import TestCreateResponse
from tgen_test.concepts.utils import create_concept_args


class TestConceptPipeline(BaseTest):
    @mock_anthropic
    def test_concept_pipeline(self, ai_manager: TestAIManager) -> None:
        """
        Tests full execution of pipeline.
        :param ai_manager: AI manager used to mock LLM calls.
        :return:None
        """
        args = create_concept_args()
        pipeline = ConceptPipeline(args)
        pipeline.run()
        res = pipeline.state.response
        TestCreateResponse.verify_response(self, res)
