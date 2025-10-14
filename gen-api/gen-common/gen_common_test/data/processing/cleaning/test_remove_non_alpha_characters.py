from gen_common.data.processing.cleaning.remove_non_alpha_chars_step import RemoveNonAlphaCharsStep
from gen_common.util.file_util import FileUtil
from gen_common_test.base.paths.project_paths import GEN_COMMON_TEST_PROJECT_CLEANING_CPP
from gen_common_test.base.tests.base_test import BaseTest


class TestRemoveNonAlphaChars(BaseTest):
    """
    Tests ability to remove non alpha numeric characters from strings.
    """

    TEST_FILE = FileUtil.read_file(GEN_COMMON_TEST_PROJECT_CLEANING_CPP)
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
