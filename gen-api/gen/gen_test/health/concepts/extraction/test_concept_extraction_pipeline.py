from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.tests.base_test import BaseTest

from gen.health.concepts.extraction.concept_extraction_pipeline import ConceptExtractionPipeline
from gen_test.health.concepts.extraction.test_define_undefined_concepts_step import TestDefineUndefinedConceptsStep
from gen_test.health.concepts.extraction.test_undefined_concept_extraction_step import TestUndefinedConceptExtractionStep
from gen_test.health.concepts.matching.utils import create_concept_args


class TestEntityExtractionPipeline(BaseTest):
    @mock_anthropic
    def test_use_case(self, ai_manager: TestAIManager):
        """
        Verifies that concept extraction pipeline can run in sequence.
        """
        args = create_concept_args()
        self.setup_data(args)
        self.mock_responses(ai_manager)

        pipeline = ConceptExtractionPipeline(args=args)
        pipeline.run()

        state = pipeline.state
        TestUndefinedConceptExtractionStep.verify_state(self, state)
        TestDefineUndefinedConceptsStep.verify_state(self, state)

    @staticmethod
    def mock_responses(ai_manager: TestAIManager) -> None:
        """
        Mocks responses to setup test environment.
        :param ai_manager: AI manager used to add responses to.
        :return: None
        """
        TestUndefinedConceptExtractionStep.mock_responses(ai_manager)
        TestDefineUndefinedConceptsStep.mock_responses(ai_manager)

    @staticmethod
    def setup_data(args) -> None:
        """
        Sets up test data.
        :param args: Arguments to concept pipeline.
        :return: None
        """
        TestUndefinedConceptExtractionStep.setup_data(args)
