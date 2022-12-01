from enum import Enum

from tracer.datasets.processing.cleaning.filter_min_length_step import FilterMinLengthStep
from tracer.datasets.processing.cleaning.manual_replace_words_step import ManualReplaceWordsStep
from tracer.datasets.processing.cleaning.remove_unwanted_chars_step import RemoveUnwantedCharsStep
from tracer.datasets.processing.cleaning.remove_white_space_step import RemoveWhiteSpaceStep
from tracer.datasets.processing.cleaning.separate_joined_words_step import SeparateJoinedWordsStep
from tracer.datasets.processing.cleaning.shuffle_words_step import ShuffleWordsStep


class DataCleaningSteps(Enum):
    FILTER_MIN_LENGTH = FilterMinLengthStep
    SHUFFLE_WORDS = ShuffleWordsStep
    REMOVE_UNWANTED_CHARS = RemoveUnwantedCharsStep
    SEPARATE_JOINED_WORDS = SeparateJoinedWordsStep
    REPLACE_WORDS = ManualReplaceWordsStep
    REMOVE_WHITE_SPACE = RemoveWhiteSpaceStep

    def get_step_attributes(self):
        for step_class in DataCleaningSteps:
            step_attributes = dir(step_class)
