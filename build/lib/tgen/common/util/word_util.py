import os
from collections.abc import Set
from os.path import dirname

import pandas as pd
from common_resources.tools.constants.symbol_constants import SPACE


def get_common_words() -> Set[str]:
    """
    Reads in a list of common words for pre-processing in nlp.
    :return: A set of common words.
    """
    return set(pd.read_csv(os.path.join(dirname(os.path.abspath(__file__)), "common-words.csv"), header=None)[0])


COMMON_WORDS = get_common_words()


def remove_common_words(input_string: str) -> str:
    """
    Removes the stop words in the string.
    :param input_string: The string to remove stopwords from.
    :return: The string without stop words.
    """
    return SPACE.join([word for word in input_string.split() if word.lower() not in COMMON_WORDS])
