import numpy as np
import pandas as pd


class DataFrameUtil:
    @staticmethod
    def convert_df(df, column_translation, drop_na=True):
        entities = []
        for i, entity_row in df.iterrows():
            entity_dict = {}
            for source_col, target_col in column_translation.items():
                source_value = entity_row[source_col]
                source_value = int(source_value) if isinstance(source_value, float) and not np.isnan(
                    source_value) else source_value
                entity_dict[target_col] = source_value
            entities.append(entity_dict)
        df = pd.DataFrame(entities)
        if drop_na:
            return df.dropna()
        return df
