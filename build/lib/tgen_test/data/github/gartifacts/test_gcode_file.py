import os

from common_resources.tools.constants.code_extensions import ALLOWED_CODE_EXTENSIONS

from common_resources.tools.util.file_util import FileUtil
from tgen.data.github.gartifacts.gcode_file import GCodeFile
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_OUTPUT_DIR


class TestGCodeFile(BaseTest):

    def test_ends_with_ext(self):
        file1 = "file.txt"
        self.assertFalse(GCodeFile.ends_with_allowed_code_ext(file1, ALLOWED_CODE_EXTENSIONS))

        file2 = "file.py"
        self.assertTrue(GCodeFile.ends_with_allowed_code_ext(file2, ALLOWED_CODE_EXTENSIONS))

    def test_get_all_code_files_with_ext(self):
        base_dir = os.path.join(TEST_OUTPUT_DIR, "base_dir")
        nested_dir = os.path.join(base_dir, "nested_dir")
        files = ["file1.py", "file2.java", "file3.txt"]
        base_files = [os.path.join(base_dir, file) for file in files]
        nested_files = [os.path.join(nested_dir, file) for file in files]

        for i, filename in enumerate(files):  # create empty files
            FileUtil.safe_open_w(base_files[i])
            FileUtil.safe_open_w(nested_files[i])

        file_paths = GCodeFile.get_all_code_files_with_ext(base_dir, ALLOWED_CODE_EXTENSIONS)
        expected_files = base_files[:2] + nested_files[:2]
        unexpected_files = [base_files[-1], nested_files[-1]]
        for file in expected_files:
            self.assertIn(file, file_paths)
        for file in unexpected_files:
            self.assertNotIn(file, file_paths)
