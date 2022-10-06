from enum import Enum

from common.pre_processing.remove_unwanted_chars_step import RemoveUnwantedCharsStep
from common.pre_processing.separate_joined_words_step import SeparateJoinedWordsStep
from common.pre_processing.shuffle_words_step import ShuffleWordsStep


class PreProcessingOptions(Enum):
    SHUFFLE_WORDS = ShuffleWordsStep
    REMOVE_UNWANTED_CHARS = RemoveUnwantedCharsStep
    SEPARATE_JOINED_WORDS = SeparateJoinedWordsStep

    @classmethod
    def get_ordered_steps(cls):
        return sorted([step for step in PreProcessingOptions], key=lambda step: step.value)
