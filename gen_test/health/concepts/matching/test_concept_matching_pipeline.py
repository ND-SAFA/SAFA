from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.tests.base_test import BaseTest

from gen.health.concepts.matching.concept_matching_pipeline import ConceptMatchingPipeline
from gen_test.health.concepts.matching.test_direct_concept_matching import TestDirectConceptMatching
from gen_test.health.concepts.matching.test_llm_concept_matching_step import TestLLMConceptMatchingStep
from gen_test.health.concepts.matching.utils import create_concept_args


class TestConceptMatchingPipeline(BaseTest):
    @mock_anthropic
    def test_concept_pipeline(self, ai_manager: TestAIManager) -> None:
        """
        Tests full execution of pipeline.
        :param ai_manager: AI manager used to mock LLM calls.
        :return:None
        """
        TestLLMConceptMatchingStep.mock_predictions(ai_manager)

        args = create_concept_args()
        pipeline = ConceptMatchingPipeline(args)

        pipeline.run()

        TestDirectConceptMatching.verify_state(self, pipeline.state)
        TestLLMConceptMatchingStep.verify_state(self, pipeline.state)
