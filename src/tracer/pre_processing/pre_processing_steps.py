from enum import Enum

from tracer.pre_processing.steps.filter_min_length_step import FilterMinLengthStep
from tracer.pre_processing.steps.remove_unwanted_chars_step import RemoveUnwantedCharsStep
from tracer.pre_processing.steps.remove_white_space_step import RemoveWhiteSpaceStep
from tracer.pre_processing.steps.replace_words_step import ReplaceWordsStep
from tracer.pre_processing.steps.separate_joined_words_step import SeparateJoinedWordsStep
from tracer.pre_processing.steps.shuffle_words_step import ShuffleWordsStep


class PreProcessingSteps(Enum):
    FILTER_MIN_LENGTH = FilterMinLengthStep
    SHUFFLE_WORDS = ShuffleWordsStep
    REMOVE_UNWANTED_CHARS = RemoveUnwantedCharsStep
    SEPARATE_JOINED_WORDS = SeparateJoinedWordsStep
    REPLACE_WORDS = ReplaceWordsStep
    REMOVE_WHITE_SPACE = RemoveWhiteSpaceStep

    def get_step_attributes(self):
        for step_class in PreProcessingSteps:
            step_attributes = dir(step_class)
