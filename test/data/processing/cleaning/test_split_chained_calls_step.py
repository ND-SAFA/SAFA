from tgen.data.processing.cleaning.split_chained_calls_tep import SplitChainedCallsStep
from tgen.testres.base_tests.base_test import BaseTest


class TestSplitChainedCallsStep(BaseTest):
    """
    Test that splits chained code calls
    """

    def test_simple_use_case(self):
        """
        Tests that single command is processed correctly.
        """
        input_phrase = "word.strip().process()"
        expected_phrase = "word strip() process()"
        step = SplitChainedCallsStep()
        resulting_phrases = step.run([input_phrase])
        self.assertSize(1, resulting_phrases)
        self.assertEqual(expected_phrase, resulting_phrases[0])
