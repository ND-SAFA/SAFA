import os

import pandas as pd
from gen_common_test.base.tests.base_test import BaseTest

from gen.data.github.repository_exporter import RepositoryExporter
from gen_test.res.paths import COMMON_TEST_GITHUB_ARTIFACTS_PATH, TEST_OUTPUT_DIR


class TestGithubExporter(BaseTest):
    """
    Tests the correctness of exporting artifacts.
    """

    def test_export(self):
        """
        Tests that all files are exported and have expected number of entities.
        """
        exporter = RepositoryExporter(COMMON_TEST_GITHUB_ARTIFACTS_PATH)
        exporter.extract(TEST_OUTPUT_DIR)
        self.assert_df_length(os.path.join(TEST_OUTPUT_DIR, "issue.csv"), 2)
        self.assert_df_length(os.path.join(TEST_OUTPUT_DIR, "pull.csv"), 1)
        self.assert_df_length(os.path.join(TEST_OUTPUT_DIR, "commit.csv"), 1)
        self.assert_df_length(os.path.join(TEST_OUTPUT_DIR, "commit2issue.csv"), 1)
        self.assert_df_length(os.path.join(TEST_OUTPUT_DIR, "commit2pull.csv"), 1)
        self.assert_df_length(os.path.join(TEST_OUTPUT_DIR, "pull2issue.csv"), 1)

    def assert_df_length(self, file_path: str, n_items: int) -> None:
        """
        Asserts that data frame at file path contains the number of items.
        :param file_path: Path to data frame file.
        :param n_items: The expected number of items.
        :return: None
        """
        df = pd.read_csv(file_path)
        self.assertEqual(n_items, len(df))
