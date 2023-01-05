from enum import Enum


class SupportedSplitStrategy(Enum):
    """
    Enum of keys enumerating supported trace dataset split methods.
    Note, values are keys instead of classes to avoid circular imports.
    """
    RANDOM = "random"
    SOURCE_RANDOM = "source_random"
