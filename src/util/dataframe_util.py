import numpy as np
import pandas as pd


class DataFrameUtil:
    @staticmethod
    def convert_columns(df, column_translation, drop_na=True):
        if column_translation is None or len(column_translation) == 0:
            column_translation = {col: col for col in df.columns}
        entities = []
        for i, entity_row in df.iterrows():
            entity_dict = {}
            for source_col, target_col in column_translation.items():
                if source_col not in entity_row:
                    continue
                source_value = entity_row[source_col]
                source_value = int(source_value) if isinstance(source_value, float) and not np.isnan(
                    source_value) else source_value
                entity_dict[target_col] = source_value
            entities.append(entity_dict)
        df = pd.DataFrame(entities)
        if drop_na:
            return df.dropna()
        return df
