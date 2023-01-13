from typing import Dict

import numpy as np
import pandas as pd


class DataFrameUtil:
    """
    Provides general operations for data frames.
    """

    @staticmethod
    def rename_columns(df: pd.DataFrame, column_translation: Dict[str, str], drop_na=True) -> pd.DataFrame:
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

        df = df.rename(column_translation, axis=1)
        df = df[list(column_translation.values())]

        if drop_na:
            return df.dropna()
        return df
