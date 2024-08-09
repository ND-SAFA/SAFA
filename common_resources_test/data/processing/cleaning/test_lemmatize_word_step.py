from common_resources.data.processing.cleaning.lemmatize_words_step import LemmatizeWordStep
from common_resources_test.base_tests.base_test import BaseTest


class TestLemmatizeWordStep(BaseTest):
    """
    Tests that words in documents are lemmatized.
    """

    def test_simple_use_case(self):
        """
        Tests simple use case.
        """
        phrase = "I worked on the data entries"
        expected = "i work on the data entri"
        step = LemmatizeWordStep()
        resulting_phrases = step.run([phrase])
        self.assertSize(1, resulting_phrases)
        self.assertEqual(expected, resulting_phrases[0])
