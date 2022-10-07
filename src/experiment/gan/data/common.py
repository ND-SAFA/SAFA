from typing import List, Tuple

import pandas as pd

from experiment.gan.constants import LABEL_PARAM, SOURCE_ID_PARAM, SOURCE_PARAM, TARGET_ID_PARAM, TARGET_PARAM


def create_data_df(sources: List[Tuple[str, str]],
                   targets: List[Tuple[str, str]],
                   label_examples: List[int]) -> pd.DataFrame:
    df = pd.DataFrame()

    df[SOURCE_ID_PARAM] = list(map(lambda a: a[0], sources))
    df[SOURCE_PARAM] = list(map(lambda a: a[1], sources))

    df[TARGET_ID_PARAM] = list(map(lambda a: a[0], targets))
    df[TARGET_PARAM] = list(map(lambda a: a[1], targets))

    df[LABEL_PARAM] = label_examples
    return df
