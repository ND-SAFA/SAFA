from enum import Enum

from gen_common.data.splitting.pre_train_split_strategy import PreTrainSplitStrategy
from gen_common.data.splitting.random_split_strategy import RandomSplitStrategy
from gen_common.data.splitting.source_split_strategy import SourceSplitStrategy


class SupportedSplitStrategy(Enum):
    """
    Enum of keys enumerating supported trace dataset split methods.
    Note, values are keys instead of classes to avoid circular imports.
    """
    SPLIT_BY_LINK = RandomSplitStrategy
    SPLIT_BY_SOURCE = SourceSplitStrategy
    PRE_TRAIN = PreTrainSplitStrategy
