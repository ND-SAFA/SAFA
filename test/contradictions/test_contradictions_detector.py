from test.contradictions.data_test_requirements import get_contradictions_dataset, EXPECTED_CONTRADICTIONS
from tgen.common.constants.deliminator_constants import COMMA
from tgen.common.util.prompt_util import PromptUtil
from tgen.contradictions.contradictions_args import ContradictionsArgs
from tgen.contradictions.contradictions_detector import ContradictionsDetector
from tgen.data.keys.structure_keys import TraceKeys, TraceRelationshipType
from tgen.prompts.prompt import Prompt
from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestContradictionsDetector(BaseTest):

    @mock_anthropic
    def test_detect_all(self, test_ai_manager: TestAIManager):
        task_prompt: Prompt = SupportedPrompts.CONTRADICTIONS_TASK.value
        response_tag = task_prompt.get_all_response_tags()[0]
        contradicting_id = "2"
        expected_contradictions = EXPECTED_CONTRADICTIONS[contradicting_id] + ["3"]
        test_ai_manager.set_responses([PromptUtil.create_xml(response_tag, COMMA.join(expected_contradictions + ["bad id"])),
                                       PromptUtil.create_xml(response_tag, "There are no contradictions"),
                                       PromptUtil.create_xml(response_tag, "No")])

        args = ContradictionsArgs(dataset=get_contradictions_dataset())
        detector = ContradictionsDetector(args)
        results = detector.detect(contradicting_id)
        self.assertEqual(results, expected_contradictions)
        # check related context added to trace dataframe
        context_link = args.dataset.trace_dataset.trace_df.get_link(source_id=contradicting_id, target_id=expected_contradictions[0])
        self.assertIsNotNone(context_link)
        self.assertEqual(context_link[TraceKeys.RELATIONSHIP_TYPE], TraceRelationshipType.CONTEXT)

        results = detector.detect("1")
        self.assertIsNone(results, expected_contradictions)

        results = detector.detect("1")
        self.assertIsNone(results, expected_contradictions)
