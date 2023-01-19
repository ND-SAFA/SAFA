from typing import Dict, List

import pandas as pd

from testres.base_test import BaseTest
from testres.test_assertions import TestAssertions
from util.dataframe_util import DataFrameUtil


class TestDataFrameUtil(BaseTest):
    """
    Tests data frame utility methods.
    """

    def test_rename_columns(self):
        """
        Tests that columns can be renamed and filtered.
        """
        conversion = {"source-col": "target-col"}
        entries = [{"source-col": 42.0}]
        new_entries = [{"target-col": 42}]
        self.verify_rename_columns(entries, new_entries, conversion)

    def test_rename_columns_empty(self):
        """
        Tests that columns assumed if no conversion is passed.
        """
        entries = [{"name": "one"}]
        self.verify_rename_columns(entries, entries)

    def test_filter_df(self):
        """
        Tests ability to filter data frame.
        """
        df = pd.DataFrame([{"name": "one"}])
        query_df = DataFrameUtil.filter_df(df, lambda r: r["name"] == "one")
        self.assertEqual(len(query_df), 1)
        query_df = DataFrameUtil.filter_df(df, lambda r: r["name"] == "two")
        self.assertEqual(len(query_df), 0)

    def test_add_optional_column(self):
        """
        Tests ability to add column when col already exists and when it doesn't.
        """
        df = pd.DataFrame([{"name": "one"}])
        query_df = DataFrameUtil.add_optional_column(df, "name", "two")
        self.assertListEqual(["name"], list(query_df.columns))
        query_df = DataFrameUtil.add_optional_column(df, "new-col", "two")
        self.assertListEqual(["name", "new-col"], list(query_df.columns))
        self.assertListEqual(["two"], list(query_df["new-col"]))

    def verify_rename_columns(self, source_entries: List[Dict], target_entries: List[Dict], conversion: Dict = None) -> None:
        """
        Verifies that data frame with entries results in target entries after applying conversion.
        :param source_entries: The entries to create original data frame to convert.
        :param target_entries: The entries expected to be present in converted data frame.
        :param conversion: Dictionary mapping source to target columns
        :return: None
        """
        source_df = pd.DataFrame(source_entries)
        target_df = DataFrameUtil.rename_columns(source_df, conversion)
        TestAssertions.verify_entities_in_df(self, target_entries, target_df)
