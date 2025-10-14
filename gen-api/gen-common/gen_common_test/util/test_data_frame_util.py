from typing import Any, Dict, List

import numpy as np
import pandas as pd

from gen_common.util.dataframe_util import DataFrameUtil
from gen_common_test.base.tests.base_test import BaseTest


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
        query_df = DataFrameUtil.filter_df_by_row(df, lambda r: r["name"] == "one")
        self.assertEqual(len(query_df), 1)
        query_df = DataFrameUtil.filter_df_by_row(df, lambda r: r["name"] == "two")
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

    def test_get_optional_value(self):
        """
        Tests the correctness of the get optional value method.
        """
        entry = {"A": 1, "B": "HI", "C": np.NAN, "D": ""}
        df = pd.DataFrame([entry])

        def assert_value(key_name: str, v: Any, **kwargs):
            value = DataFrameUtil.get_optional_value_from_df(df.iloc[0], key_name, **kwargs)
            self.assertEqual(value, v)

        assert_value("A", 1)
        assert_value("B", "HI")
        assert_value("C", None)
        assert_value("D", "")
        assert_value("D", None, allow_empty=False)

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
        self.verify_entities_in_df(target_entries, target_df)

    def test_contains_empty_string(self):
        df = pd.DataFrame({"id": [1, 2], "column1": ["hello", ""]})
        self.assertTrue(DataFrameUtil.contains_empty_string(df["column1"]))
        df = pd.DataFrame({"id": [1, 2], "column1": ["hello", "world"]})
        self.assertFalse(DataFrameUtil.contains_empty_string(df))

    def test_find_nan_empty_indices(self):
        expected_empty_indices = [2, 4, 5]
        df = pd.DataFrame({"column": [1, 2, np.NaN, 3, "", None]})
        empty_indices = DataFrameUtil.find_nan_empty_indices(df["column"])
        self.assertListEqual(expected_empty_indices, empty_indices)
