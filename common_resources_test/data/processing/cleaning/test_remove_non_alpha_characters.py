from common_resources.data.processing.cleaning.remove_non_alpha_chars_step import RemoveNonAlphaCharsStep
from common_resources_test.base_tests.base_test import BaseTest
from common_resources_test.paths.base_paths import TEST_FILE_PATH
from common_resources.tools.util.file_util import FileUtil


class TestRemoveNonAlphaChars(BaseTest):
    """
    Tests ability to remove non alpha numeric characters from strings.
    """

    TEST_FILE = FileUtil.read_file(TEST_FILE_PATH)
    EXPECTED_REMOVED_STRINGS = ["@brief", "//", "{"]

    def test_expected_strings_are_removed(self):
        """
        Tests that the non-alpha numeric strings defined are successfully removed from file.
        """
        for expected_removed_str in self.EXPECTED_REMOVED_STRINGS:
            self.assertIn(expected_removed_str, self.TEST_FILE)

        step = RemoveNonAlphaCharsStep()
        cleaned_files = step.run([self.TEST_FILE])
        self.assertSize(1, cleaned_files)

        for cleaned_file in cleaned_files:
            for expected_removed_str in self.EXPECTED_REMOVED_STRINGS:
                self.assertTrue(expected_removed_str not in cleaned_file)
