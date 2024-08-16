from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union

import numpy as np
import pandas as pd

from gen_common.constants import EMPTY_STRING


class DataFrameUtil:
    """
    Provides general operations for data frames.
    """

    @staticmethod
    def rename_columns(df: pd.DataFrame, column_translation: Dict[str, str] = None) -> pd.DataFrame:
        """
        Renames the columns of the data frame.
        :param df: The data frame whose columns should be renamed.
        :param column_translation: Mapping from source to target column names.
        :return: DataFrame with columns converted and na's dropped (when specified)
        """
        if column_translation is None or len(column_translation) == 0:
            column_translation = {col: col for col in df.columns}

        column_translation = {k: v for k, v in column_translation.items() if k in df.columns}
        df = df[column_translation.keys()]
        df = df.rename(column_translation, axis=1)
        df = df[list(column_translation.values())]

        return df

    @staticmethod
    def filter_df_by_row(df: pd.DataFrame, filter_lambda: Callable[[pd.Series], bool]) -> pd.DataFrame:
        """
        Returns DataFrame containing rows returning true in filter.
        :param df: The original DataFrame.
        :param filter_lambda: The lambda determining which rows to keep.
        :return: DataFrame containing filtered rows.
        """
        filter_df = df.apply(filter_lambda, axis=1)
        return df[filter_df]

    @staticmethod
    def filter_df_by_index(df: pd.DataFrame, index_to_filter: List[Any]) -> pd.DataFrame:
        """
         Returns DataFrame containing rows if index not in index_to_filter.
         :param df: The original DataFrame.
         :param index_to_filter: The list of indices to filter out.
         :return: DataFrame containing filtered rows.
         """
        return df[df.index.isin(index_to_filter)]

    @staticmethod
    def query_df(df: pd.DataFrame, query: Dict):
        """
        Filters the dataframe to match the given query
        :param df: The dataframe to query
        :param query: Dictionary mapping query key to the desired value.
        :return: The filtered dataframe
        """
        query_df = df
        for k, v in query.items():
            if v is None:
                continue
            if isinstance(v, str) and len(v) == 0:  # e.g. summary is empty in query but df contains NA
                continue

            if k == df.index.name:
                query_df = df.loc[[v]]
            elif k in query_df.columns:
                query_df = query_df[query_df[k] == v]
            else:
                raise ValueError(f"{query_df} does not have key: {k}")

        return query_df

    @staticmethod
    def add_optional_column(df: pd.DataFrame, col_name: str, default_value: Any) -> pd.DataFrame:
        """
        Adds default value to column if not found in data frame.
        :param df: The data frame to modify.
        :param col_name: The name of the column to verify or add.
        :param default_value: The value of the column if creating new one.
        :return: None
        """
        df = df.copy()
        if col_name not in df.columns:
            df[col_name] = [default_value] * len(df)
        return df

    @staticmethod
    def append(df_dict: Dict, col2value: Dict) -> Dict:
        """
        Replaces old append method in panda dataframe by adding rows to the dictionary which can be used to initialize the df
        :param df_dict: dictionary representing the dataframe
        :param col2value: maps column name to value
        :return: the updated dictionary
        """
        for col, value in col2value.items():
            if col not in df_dict:
                df_dict[col] = []
            df_dict[col].append(value)
        return df_dict

    @staticmethod
    def get_optional_value_from_df(row: Union[pd.Series, Dict], col_name: Union[str, Enum],
                                   allow_empty: bool = True, default_value: Any = None) -> Optional[Any]:
        """
        Returns the column value if exists, otherwise None is returned.
        :param row: The row in the dataframe.
        :param col_name: The name of the column.
        :param allow_empty: Whether to allow empty string. If false, None is returned on empty string.
        :param default_value: The value to use as a default if the value does not exist.
        :return: The column value if exists, otherwise None is returned.
        """
        potential_value = row.get(col_name, default_value)
        result = DataFrameUtil.get_optional_value(potential_value, allow_empty)
        return result if result is not None else default_value

    @staticmethod
    def get_optional_value(potential_value: Any, allow_empty: bool = True) -> Optional[Any]:
        """
        Returns the potential_value value if exists, otherwise None is returned.
        :param potential_value: The potential value which may or may not exist
        :param allow_empty: Whether to allow empty string. If false, None is returned on empty string.
        :return: The potential value if it
        """
        if potential_value is not None:
            if isinstance(potential_value, float):
                if np.isnan(potential_value):
                    return None
                return potential_value
            if isinstance(potential_value, str):
                if not allow_empty:
                    return potential_value if len(potential_value) > 0 else None
            return potential_value
        else:
            return None

    @staticmethod
    def contains_na(df: pd.DataFrame) -> bool:
        """
        Returns whether the dataframe contains any NAN values
        :param df: The dataframe to evaluate
        :return: True if the dataframe contains any NAN values
        """
        return df.isna().any()

    @staticmethod
    def contains_empty_string(df: pd.Series) -> bool:
        """
        Returns whether data frame or series contains any empty strings.
        :param df: The data to check.
        :return: True if empty strings is found, False otherwise.
        """
        query = np.where(df.apply(lambda x: x == EMPTY_STRING))
        return len([1 for q in query if len(q) > 0]) > 0

    @staticmethod
    def find_nan_empty_indices(df: pd.Series) -> List:
        """
        Returns the indices where the data frame or series has empty strings or nan.
        :param df: The data to check.
        :return: List of indices without values.
        """
        nan_empty_indices = df.apply(lambda x: pd.isna(x) or x == EMPTY_STRING)

        nan_empty_indices = nan_empty_indices[nan_empty_indices].index
        return list(nan_empty_indices)
