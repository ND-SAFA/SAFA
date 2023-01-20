from typing import Any, Callable, Dict

import numpy as np
import pandas as pd


class DataFrameUtil:
    """
    Provides general operations for data frames.
    """

    @staticmethod
    def rename_columns(df: pd.DataFrame, column_translation: Dict[str, str] = None, drop_na=True) -> pd.DataFrame:
        """
        Renames the columns of the data frame.
        :param df: The data frame whose columns should be renamed.
        :param column_translation: Mapping from source to target column names.
        :param drop_na: Whether to drop entries containing na values.
        :return: DataFrame with columns converted and na's dropped (when specified)
        :rtype:
        """
        if column_translation is None or len(column_translation) == 0:
            column_translation = {col: col for col in df.columns}

        for df_col in df.select_dtypes(include=[float]).columns:
            df[df_col] = df[df_col].map(lambda v: int(v) if isinstance(v, float) and not np.isnan(v) else v)
        df = df[column_translation.keys()]
        df = df.rename(column_translation, axis=1)
        df = df[list(column_translation.values())]

        if drop_na:
            return df.dropna()
        return df

    @staticmethod
    def filter_df(df: pd.DataFrame, filter_lambda: Callable[[pd.Series], bool]) -> pd.DataFrame:
        """
        Returns DataFrame containing rows returning true in filter.
        :param df: The original DataFrame.
        :param filter_lambda: The lambda determining which rows to keep.
        :return: DataFrame containing filtered rows.
        """
        return df[df.apply(filter_lambda, axis=1)]

    @staticmethod
    def query_df(df: pd.DataFrame, query: Dict):
        query_df = df
        for k, v in query.items():
            query_df = query_df[query_df[k] == v]
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
