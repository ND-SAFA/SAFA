from typing import List, Set, Tuple

from analysis import word_tools
from analysis.word_tools import WordCounter
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from spellchecker import SpellChecker
from nltk.corpus import wordnet as wn

from models.model_manager import ModelManager

nltk.download('wordnet', quiet=True)


class LinkAnalyzer:
    """
     Handles analysis of a trace link
     """

    def __init__(self, link: TraceLink):
        """
         Initializes the analyzer for analysis of given link
        :param link: The link to analyze
        """
        self.link = link
        self.vocabs = [self.get_artifact_vocab(link.source), self.get_artifact_vocab(link.target)]
        self.word_counts = [WordCounter(vocab).filter_stop_words() for vocab in self.vocabs]

    def get_words_in_common(self) -> Set[str]:
        """
        Gets the set of words that are shared between the two artifacts
        :return: The intersecting set of words
        """
        return self.word_counts[0].intersection(self.word_counts[1])

    def get_misspelled_words(self) -> List[str]:
        """
        Gets the misspelled words from the artifacts
        :return: The list of misspelled words
        """
        spell = SpellChecker()
        misspelled = []
        for word_count in self.word_counts:
            misspelled.extend(spell.unknown(list[word_count.get_word_set()]))
        return misspelled

    def get_shared_synonyms_and_antonyms(self) -> Tuple[Set[str], Set[str]]:
        """
        Gets the set of shared synonyms and antonyms between artifacts
        :return: The set of shared synonyms and antonyms
        """
        synonyms, antonyms = self.get_synonyms_and_antonyms(self.word_counts[0])
        shared_synonyms = self.word_counts[1].intersection(synonyms)
        shared_antonyms = self.word_counts[1].intersection(antonyms)
        return shared_synonyms, shared_antonyms

    def get_oov_words(self, model_manager: ModelManager) -> "WordCounter":
        """
        Gets all the OOV words from the artifacts
        :param model_manager: The model to compare vocab to
        :return The set of OOV words
        """
        oov_words = WordCounter()  # TODO
        for word_count in self.word_counts:
            oov_words.update(word_count.get_oov_words(model_manager))
        return oov_words

    @staticmethod
    def get_synonyms_and_antonyms(vocab: List[str]) -> Tuple[Set[str], Set[str]]:
        """
        Gets the synonyms from the vocab
        :param vocab: The vocab to get all synonyms for
        :return: A set of synonyms for the vocab
        """
        synonyms = set()
        antonyms = set()
        for word in vocab:
            for synset in wn.synsets(word):
                for lemma in synset.lemmas():
                    synonyms.add(lemma.name())
                    if lemma.antonyms():
                        antonyms.add(lemma.antonyms()[0].name())
        return synonyms, antonyms

    @staticmethod
    def get_artifact_vocab(artifact: Artifact) -> List[str]:
        """
        Gets the vocabulary of the artifact
        :param artifact: The artifact to get vocab of
        :return: The vocabulary of the artifact
        """
        artifact_body = word_tools.CLEANER.run([artifact.token.lower()]).pop()
        return artifact_body.split()
