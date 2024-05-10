from test.contradictions.data_test_requirements import get_contradictions_dataset, EXPECTED_CONTRADICTIONS
from tgen.common.constants.deliminator_constants import COMMA
from tgen.common.util.prompt_util import PromptUtil
from tgen.contradictions.contradictions_args import ContradictionsArgs
from tgen.contradictions.contradictions_detector import ContradictionsDetector
from tgen.data.keys.structure_keys import TraceKeys, TraceRelationshipType
from tgen.prompts.questionnaire_prompt import QuestionnairePrompt
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestContradictionsDetector(BaseTest):

    @mock_anthropic
    def test_detect_all(self, test_ai_manager: TestAIManager):
        task_prompt: QuestionnairePrompt = SupportedPrompts.CONTRADICTIONS_TASK.value
        contradictions_tag = task_prompt.get_response_tags_for_prompt(0)
        explanation_tag = task_prompt.get_response_tags_for_prompt(1)
        contradicting_id = "2"
        explanation = "This is why there is a contradiction."
        test_ai_manager.set_responses(
            [PromptUtil.create_xml(contradictions_tag, COMMA.join(EXPECTED_CONTRADICTIONS[contradicting_id] + ["3", "bad id"])) +
             PromptUtil.create_xml(explanation_tag, explanation),
             PromptUtil.create_xml(contradictions_tag, "There are no contradictions"),
             PromptUtil.create_xml(contradictions_tag, "No")])

        args = ContradictionsArgs(dataset=get_contradictions_dataset())
        detector = ContradictionsDetector(args)
        results = detector.detect(contradicting_id)
        self.assertEqual(results["conflicting_ids"], EXPECTED_CONTRADICTIONS[contradicting_id])
        self.assertEqual(results["explanation"], explanation)
        # check related context added to trace dataframe
        context_link = args.dataset.trace_dataset.trace_df.get_link(source_id=contradicting_id,
                                                                    target_id=EXPECTED_CONTRADICTIONS[contradicting_id][0])
        self.assertIsNotNone(context_link)
        self.assertEqual(context_link[TraceKeys.RELATIONSHIP_TYPE], TraceRelationshipType.CONTEXT)

        results = detector.detect("1")
        self.assertIsNot(results["conflicting_ids"], EXPECTED_CONTRADICTIONS[contradicting_id])
        self.assertFalse(results["explanation"])

        results = detector.detect("1")
        self.assertIsNot(results, EXPECTED_CONTRADICTIONS[contradicting_id])
        self.assertIsNot(results["conflicting_ids"], EXPECTED_CONTRADICTIONS[contradicting_id])
        self.assertFalse(results["explanation"])
