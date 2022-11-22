import random
from copy import copy
from dataclasses import dataclass
from typing import List, Set, Optional

import nltk
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords

Synset = nltk.corpus.reader.wordnet.Synset


@dataclass
class WordRepresentation:
    word: str
    is_stop_word: bool
    pos: str
    replacements: Set[str]
    is_end_of_sentence: bool = False


class DataAugmenter:
    POS2EXCLUDE = {wn.NOUN}
    STOPWORDS = set(stopwords.words('english'))
    NEW_LINE = "\n"
    lemmatizer = WordNetLemmatizer()

    def __init__(self, replacement_rate: float):
        """
        Handles data augmentation to obtain a larger dataset
        :param replacement_rate: the rate at which to replace words
        """
        self.replacement_rate = replacement_rate

    def run(self, data_entries: List[str], n_expected: int) -> List[str]:
        """
        Runs the data augmentation to obtain a larger dataset
        :param data_entries: a list of data content
        :param n_expected: the number of data entries desired
        :return: the augmented data
        """
        n_orig = len(data_entries)
        n_sample = self._get_number_to_sample(n_orig, n_orig, n_expected)
        augmented_data = copy(data_entries)
        while n_sample > 0:
            for entry in random.sample(data_entries, k=n_sample):
                augmented_data.append(self._generate_new_content(entry))
            n_sample = self._get_number_to_sample(n_orig, len(augmented_data), n_expected)
        return augmented_data

    @staticmethod
    def _get_number_to_sample(n_orig: int, n_total: int, n_expected: int):
        n_sample = n_total - n_expected
        return n_sample if n_sample <= n_total else n_orig

    def _generate_new_content(self, orig_content: str) -> str:
        """
        Generates new content by replacing words in the original content
        :return: the new content
        """
        word_reps = self._to_word_representations(orig_content)
        n_replacements = int(len(word_reps) * self.replacement_rate)
        indices2replace = set(random.sample([i for i in range(len(word_reps)) if self._should_replace(word_reps[i])],
                                            k=n_replacements))
        new_content = []
        for i, wr in enumerate(word_reps):
            word = wr.replacements.pop() if i in indices2replace else wr.word
            new_content.append(word)
            if wr.is_end_of_sentence:
                new_content.append("\n")
        return " ".join(new_content)

    @staticmethod
    def _get_word_pos(tag) -> Optional[str]:
        """
        Gets the part of speech from the word's tag
        :param tag: the word tag generated from nltk pos_tag
        :return: the part of speech
        """
        if tag.startswith('J'):
            return wn.ADJ
        elif tag.startswith('N'):
            return wn.NOUN
        elif tag.startswith('R'):
            return wn.ADV
        elif tag.startswith('V'):
            return wn.VERB
        return None

    @staticmethod
    def _get_synonyms(orig_word: str, pos: str) -> Set[str]:
        """
        Gets all possible synonyms for a word
        :param orig_word: the original word
        :param pos: the part of speech
        :return: a set of synonyms
        """
        synsets = wn.synsets(DataAugmenter.lemmatizer.lemmatize(orig_word), pos=pos) if pos else []
        return {name for syn in synsets for name in syn.lemma_names() if name != orig_word}

    @staticmethod
    def _to_word_representations(orig_content: str) -> List[WordRepresentation]:
        """
        Converts all words in the content into word representations
        :param orig_content: the original content
        :return: the content as a list of word representations
        """
        word_representations = []
        for sentence in orig_content.splitlines():
            sentence_word_reps = []
            tokens = word_tokenize(sentence)
            for word, tag in pos_tag(tokens):
                pos = DataAugmenter._get_word_pos(tag)
                replacements = DataAugmenter._get_synonyms(word, pos)
                sentence_word_reps.append(WordRepresentation(word=word, pos=pos, replacements=replacements,
                                                             is_stop_word=word in DataAugmenter.STOPWORDS))
            last_word = sentence_word_reps.pop()
            last_word.is_end_of_sentence = True
            sentence_word_reps.append(last_word)
            word_representations.extend(sentence_word_reps)
        return word_representations

    @staticmethod
    def _should_replace(word_rep: WordRepresentation) -> bool:
        """
        Determine if the word should be replaced
        :param word_rep: the word representation
        :return: True if the word should be replaced else False
        """
        return word_rep.replacements and not word_rep.is_stop_word and word_rep.pos not in DataAugmenter.POS2EXCLUDE
