from test.concepts.test_create_response import TestCreateResponse
from test.concepts.test_entity_extraction import TestEntityExtraction
from test.concepts.test_entity_matching import TestEntityMatching
from test.concepts.utils import create_concept_args, create_concept_test_entities
from tgen.concepts.concept_pipeline import ConceptPipeline
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_openai import mock_openai
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestConceptPipeline(BaseTest):
    @mock_openai
    def test_concept_pipeline(self, ai_manager: TestAIManager) -> None:
        """
        Tests full execution of pipeline.
        :param ai_manager: AI manager used to mock LLM calls.
        :return:None
        """
        args = create_concept_args()
        test_entity_df = create_concept_test_entities()

        TestEntityExtraction.mock_entity_extraction(ai_manager, test_entity_df)
        TestEntityMatching.mock_entity_matching(ai_manager)

        # Execution
        pipeline = ConceptPipeline(args)
        pipeline.run()
        res = pipeline.state.response
        TestCreateResponse.verify_response(self, res)
