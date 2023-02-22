import string
from collections import Counter
from typing import Iterable, Dict, Callable, List, Union, Set

from data.processing.cleaning.data_cleaner import DataCleaner
from data.processing.cleaning.remove_unwanted_chars_step import RemoveUnwantedCharsStep
from data.processing.cleaning.remove_white_space_step import RemoveWhiteSpaceStep
from data.processing.cleaning.separate_joined_words_step import SeparateJoinedWordsStep
from spellchecker import SpellChecker
import nltk
from nltk.corpus import stopwords

from models.model_manager import ModelManager

nltk.download('stopwords', quiet=True)

STOP_WORDS = set(stopwords.words('english'))
CLEANER = DataCleaner([RemoveWhiteSpaceStep(), SeparateJoinedWordsStep(),
                       RemoveUnwantedCharsStep(additional_unwanted_chars=string.punctuation + string.digits)])


class WordCounter(Counter):

    def __init__(self, words: Iterable[str] = None):
        """
        Initializes the word counter with the counts of the given words
        :param words: The words to get counts for
        """
        super().__init__(words)

    def total(self) -> int:
        """
        Gets the total number of elements in the counter
        :return: The total
        """
        return sum(self.values())

    def as_dict(self) -> Dict[str, int]:
        """
        Gets the word counter as a dictionary
        :return: A dictionary mapping word to its count
        """
        return dict(self)

    @staticmethod
    def from_dict(word_counts: Dict[str, int]) -> "WordCounter":
        """
        Creates a counter from a dictionary mapping words to their counts
        :param word_counts: A dictionary mapping words to their counts
        :return: The counter
        """
        return WordCounter(word_counts)

    def filter(self, criteria: Callable) -> "WordCounter":
        """
        Gets all words and their count if the count meets the criteria
        :param criteria: A callable that returns True if criteria is met
        :return: A dictionary of words and their count if the count meets the criteria
        """
        return WordCounter.from_dict({word: count for word, count in self.items() if criteria(word, count)})

    def filter_stop_words(self):
        """
        Filters all words that are considered stopwords by nltk
        :return: A dictionary of words and their count if the word is not a stopword
        """
        return self.filter(lambda word, _: word not in STOP_WORDS)

    def get_word_set(self) -> Set[str]:
        """
        Gets the set of unique words in the word counter
        :return: The set of unique words
        """
        return set(self.keys())

    def intersection(self, other: Union["WordCounter", Set[str]]) -> "WordCounter":
        """
        Gets the intersection of words between self and other
        :param other: The other word counter or a set of words
        :return: The intersecting set of words
        """
        if not isinstance(other, WordCounter):
            other = WordCounter(other)
        intersecting_words = self.get_word_set().intersection(other)
        return WordCounter({word: self[word] + other[word] for word in intersecting_words})

    def difference(self, other: Union["WordCounter", Set[str]]) -> "WordCounter":
        """
        Gets the words that are in this set but not the others
        :param other: The other word counter or a set of words
        :return: The difference for the set of words
        """
        if not isinstance(other, WordCounter):
            other = WordCounter(other)
        difference = self.get_word_set().difference(other.get_word_set())
        return WordCounter({word: self[word] for word in difference})

    def get_oov_words(self, model_manager: ModelManager) -> "WordCounter":
        """
        Gets all the OOV words from the words
        :param model_manager: The model to compare vocab to
        :return The set of OOV words
        """
        model_vocab = model_manager.get_tokenizer().vocab.keys()
        vocab = self.get_word_set()
        oov_words = vocab.difference(model_vocab)
        return WordCounter.from_dict({word: self[word] for word in oov_words})

    def get_misspelled_words(self) -> "WordCounter":
        """
        Gets the misspelled words from the artifacts
        :return: The list of misspelled words
        """
        spell = SpellChecker()
        return WordCounter({word: self[word] for word in spell.unknown(list(self.get_word_set()))})

