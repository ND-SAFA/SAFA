from unittest import skip

from common_resources.data.processing.cleaning.extract_code_identifiers import ExtractCodeIdentifiersStep
from common_resources_test.base_tests.base_test import BaseTest
from common_resources_test.paths.base_paths import TEST_JAVA_PATH
from common_resources.tools.util.file_util import FileUtil


@skip("Skipping because of the javac parser package problems")
class TestExtractCodeIdentifiersStep(BaseTest):
    """
    Tests that extracting code identifiers processes supported formats and ignores non-code blocks.
    """

    def test_non_code(self):
        """
        Tests that non-code is ignored. Note, currently I had to choose whether we wanted
        to keep those for both cases or remove them, I went with the latter.
        """
        non_code = "hello, my name is robot and I am a dog."
        expected_response = "hello my name is robot and I am a dog"
        step = ExtractCodeIdentifiersStep()
        resulting_docs = step.run([non_code])
        self.assertEqual(resulting_docs[0], expected_response)

    def test_code(self):
        """
        Tests that identifiers from code are passed through.
        """
        code = FileUtil.read_file(TEST_JAVA_PATH)
        expected_codes = ["Abstract Base class for both virtual and physical drones",
                          "basePosition",
                          "getLongitude",
                          "Set base coordinates for the drone"]
        step = ExtractCodeIdentifiersStep()
        resulting_docs = step.run([code])
        for expected_code in expected_codes:
            self.assertIn(expected_code, resulting_docs[0])
