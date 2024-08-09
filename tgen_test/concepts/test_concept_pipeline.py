from tgen_test.concepts.constants import ConceptData
from tgen_test.concepts.test_create_response import TestCreateResponse
from tgen_test.concepts.test_define_unknown_entities import TestDefineUnknownEntities
from tgen_test.concepts.test_entity_extraction import TestPredictEntityStep
from tgen_test.concepts.test_entity_matching import TestEntityMatching
from tgen_test.concepts.utils import create_concept_args
from tgen.concepts.concept_pipeline import ConceptPipeline
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestConceptPipeline(BaseTest):
    @mock_anthropic
    def test_concept_pipeline(self, ai_manager: TestAIManager) -> None:
        """
        Tests full execution of pipeline.
        :param ai_manager: AI manager used to mock LLM calls.
        :return:None
        """
        args = create_concept_args()
        test_entity_data_frames = ConceptData.get_entity_dataframes()

        # Mock: Entity Extraction
        for test_entity_df in test_entity_data_frames:
            TestPredictEntityStep.mock_entity_extraction(ai_manager, test_entity_df)
        # MOck: Entity Matching
        TestEntityMatching.mock_entity_matching(ai_manager)
        # Mock: Undefined Entities
        entity_definitions = ConceptData.Entities.get_expected_definitions()
        TestDefineUnknownEntities.mock_entity_definitions(ai_manager, entity_definitions, tc=self)

        # Execution
        pipeline = ConceptPipeline(args)
        pipeline.run()
        res = pipeline.state.response
        TestCreateResponse.verify_response(self, res)
