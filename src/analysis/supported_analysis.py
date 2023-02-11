from enum import Enum
from typing import List


class SupportedDatasetAnalysisSteps(Enum):
    HIGH_FREQ_WORD_COUNTS = "get_high_frequency_word_counts"
    LOW_FREQ_WORD_COUNTS = "get_low_frequency_word_counts"
    OOV_WORDS = "get_oov_words"
    WORD_COUNTS = "get_word_counts"
    READABILITY_SCORE = "get_readability_score"


    @staticmethod
    def get_all() -> List["SupportedDatasetAnalysisSteps"]:
        """
        Gets all supported dataset analysis
        :return: All supported dataset analysis
        """
        return [e for e in SupportedDatasetAnalysisSteps]
