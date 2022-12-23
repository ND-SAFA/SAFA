from enum import Enum

from data.processing.cleaning.filter_min_length_step import FilterMinLengthStep
from data.processing.cleaning.manual_replace_words_step import ManualReplaceWordsStep
from data.processing.cleaning.remove_unwanted_chars_step import RemoveUnwantedCharsStep
from data.processing.cleaning.remove_white_space_step import RemoveWhiteSpaceStep
from data.processing.cleaning.separate_joined_words_step import SeparateJoinedWordsStep
from data.processing.cleaning.shuffle_words_step import ShuffleWordsStep


class SupportedDataCleaningStep(Enum):
    FILTER_MIN_LENGTH = FilterMinLengthStep
    SHUFFLE_WORDS = ShuffleWordsStep
    REMOVE_UNWANTED_CHARS = RemoveUnwantedCharsStep
    SEPARATE_JOINED_WORDS = SeparateJoinedWordsStep
    REPLACE_WORDS = ManualReplaceWordsStep
    REMOVE_WHITE_SPACE = RemoveWhiteSpaceStep
