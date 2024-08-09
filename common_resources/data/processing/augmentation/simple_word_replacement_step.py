import math
import random
from dataclasses import dataclass
from typing import List, Optional, Set, Tuple

import nltk
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords, wordnet as wn
from nltk.stem import WordNetLemmatizer

from common_resources.tools.constants.dataset_constants import REPLACEMENT_PERCENTAGE_DEFAULT
from common_resources.data.processing.augmentation.abstract_data_augmentation_step import AbstractDataAugmentationStep

Synset = nltk.corpus.reader.wordnet.Synset

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)


@dataclass
class WordRepresentation:
    word: str
    is_stop_word: bool
    pos: str
    replacements: Set[str]
    is_end_of_sentence: bool = False


class SimpleWordReplacementStep(AbstractDataAugmentationStep):
    POS2EXCLUDE = {wn.NOUN}
    STOPWORDS = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    def __init__(self, percent_to_weight: float = 1, replacement_percentage: float = REPLACEMENT_PERCENTAGE_DEFAULT):
        """
        Handles word replacement to augment the data and obtain a larger dataset
        :param percent_to_weight: the percentage of the data that the augmentation step will augment
        :param replacement_percentage: the rate at which to replace words
        """
        self.replacement_rate = replacement_percentage
        super().__init__(percent_to_weight)

    def _augment(self, data_entry: Tuple[str, str]) -> Tuple[str]:
        """
        Augments the source and target tokens through word replacement
        :param data_entry: the original content of the source and target
        :return: the new content of the source and target
        """
        augmented_content = []
        for orig_content in data_entry:
            augmented_content.append(self._augment_content(orig_content))
        return tuple(augmented_content)

    def _augment_content(self, orig_content: str) -> str:
        """
        Generates new content by replacing words in the original content
        :param orig_content: the original content
        :return: the new content
        """
        word_reps = SimpleWordReplacementStep._to_word_representations(orig_content)
        indices2sample = [i for i in range(len(word_reps)) if SimpleWordReplacementStep._should_replace(word_reps[i])]
        n_replacements = min(math.ceil(len(word_reps) * self.replacement_rate), len(indices2sample))
        indices2replace = set(random.sample(indices2sample, k=n_replacements))
        new_content = []
        for i, wr in enumerate(word_reps):
            word = wr.replacements.pop() if i in indices2replace else wr.word
            new_content.append(word)
        return SimpleWordReplacementStep.reconstruct_content(new_content)

    @staticmethod
    def _get_synonyms(orig_word: str, pos: str) -> Set[str]:
        """
        Gets all possible synonyms for a word
        :param orig_word: the original word
        :param pos: the part of speech
        :return: a set of synonyms
        """
        synsets = wn.synsets(SimpleWordReplacementStep.lemmatizer.lemmatize(orig_word), pos=pos) if pos else []
        return {name for syn in synsets for name in syn.lemma_names() if name.lower() != orig_word.lower()}

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
            word_tag_pairs = pos_tag(word_tokenize(sentence))
            for word, tag in word_tag_pairs:
                pos = SimpleWordReplacementStep._get_word_pos(tag)
                replacements = SimpleWordReplacementStep._get_synonyms(word, pos)
                sentence_word_reps.append(WordRepresentation(word=word, pos=pos, replacements=replacements,
                                                             is_stop_word=word in SimpleWordReplacementStep.STOPWORDS))
            if len(sentence_word_reps) > 0:
                last_word = sentence_word_reps.pop()
                last_word.is_end_of_sentence = True
                sentence_word_reps.append(last_word)
            word_representations.extend(sentence_word_reps)
        return word_representations

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
    def _should_replace(word_rep: WordRepresentation) -> bool:
        """
        Determine if the word should be replaced
        :param word_rep: the word representation
        :return: True if the word should be replaced else False
        """
        return not word_rep.is_stop_word and word_rep.pos not in SimpleWordReplacementStep.POS2EXCLUDE and len(
            word_rep.replacements) >= 1
