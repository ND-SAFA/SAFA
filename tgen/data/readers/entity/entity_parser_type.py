from typing import Callable, Type

import pandas as pd

EntityParserType = Type[Callable[[str], pd.DataFrame]]
