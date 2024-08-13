from common_resources.data.processing.cleaning.separate_camel_case_step import SeparateCamelCaseStep
from tgen.testres.base_tests.base_test import BaseTest


class TestSeparateCamelCase(BaseTest):
    """
    Tests that strings containing camel case words are identified and separated into individual words.
    """

    def test_simple_case(self):
        """
        Tests that simple word is processed.
        """
        test_phrase = "hello, this wordHasACamelCaseWord andThisOne"
        expected_phrase = "hello, this word Has A Camel Case Word and This One"
        step = SeparateCamelCaseStep()
        result_phrase = step.run([test_phrase])
        self.assertSize(1, result_phrase)
        self.assertEqual(expected_phrase, result_phrase[0])
