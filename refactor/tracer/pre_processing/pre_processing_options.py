from enum import Enum

from tracer.pre_processing.filter_min_length_step import FilterMinLengthStep
from tracer.pre_processing.remove_unwanted_chars_step import RemoveUnwantedCharsStep
from tracer.pre_processing.replace_words_step import ReplaceWordsStep
from tracer.pre_processing.separate_joined_words_step import SeparateJoinedWordsStep
from tracer.pre_processing.shuffle_words_step import ShuffleWordsStep


class PreProcessingOptions(Enum):
    FILTER_MIN_LENGTH = FilterMinLengthStep
    SHUFFLE_WORDS = ShuffleWordsStep
    REMOVE_UNWANTED_CHARS = RemoveUnwantedCharsStep
    SEPARATE_JOINED_WORDS = SeparateJoinedWordsStep
    REPLACE_WORDS = ReplaceWordsStep
