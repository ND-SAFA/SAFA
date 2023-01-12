from enum import Enum

from data.datasets.splitting.all_artifact_split_strategy import AllArtifactSplitStrategy
from data.datasets.splitting.all_sources_split_strategy import AllSourcesSplitStrategy
from data.datasets.splitting.combination_split_strategy import CombinationSplitStrategy
from data.datasets.splitting.random_split_strategy import RandomSplitStrategy
from data.datasets.splitting.source_split_strategy import SourceSplitStrategy


class SupportedSplitStrategy(Enum):
    """
    Enum of keys enumerating supported trace dataset split methods.
    Note, values are keys instead of classes to avoid circular imports.
    """
    RANDOM = RandomSplitStrategy
    SOURCE = SourceSplitStrategy
    COMBINATION = CombinationSplitStrategy
    RANDOM_ALL_SOURCES = AllSourcesSplitStrategy
    RANDOM_ALL_ARTIFACTS = AllArtifactSplitStrategy
