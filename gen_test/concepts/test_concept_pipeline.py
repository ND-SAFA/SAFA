from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.tests.base_test import BaseTest

from gen.concepts.concept_pipeline import ConceptPipeline
from gen_test.concepts.test_create_response import TestCreateResponse
from gen_test.concepts.utils import create_concept_args


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
