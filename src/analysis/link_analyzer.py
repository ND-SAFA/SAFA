import os
from threading import Lock
from typing import Any, Dict, List, Set, Tuple

import nltk
from nltk.corpus import wordnet as wn

from analysis import word_tools
from analysis.word_tools import WordCounter
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from models.model_manager import ModelManager
from scripts.modules.analysis_types import JobAnalysis, LinkMetrics
from util.file_util import FileUtil

nltk.download('wordnet', quiet=True)
next(wn.all_synsets())
next(wn.all_lemma_names())
wn.ensure_loaded()


class LinkAnalyzer:
    """
     Handles analysis of a trace link
     """

    COMMON_WORDS = "common_words"
    MISSPELLED_WORDS = "misspelled_words"
    SHARED_SYNONYMS = "shared_antonyms"
    SHARED_ANTONYMS = "shared_synonyms"
    OOV_WORDS = "oov_words"
    DIFF_FROM_PREDICTION_SCORE = "difference_from_prediction_score"

    ARTIFACT_TOKENS = "artifact_tokens"
    ANALYSIS = "analysis"
    LINK_TRUE_LABEL = "link_true_label"

    OUTPUT_FILENAME = "link_{}_analysis.json"

    def __init__(self, link: TraceLink, predicted_score: float, model_manager: ModelManager = None):
        """
         Initializes the analyzer for analysis of given link
        :param link: The link to analyze
        """
        self.link = link
        self.vocabs = [self.get_artifact_vocab(link.source), self.get_artifact_vocab(link.target)]
        self.word_counts = [WordCounter(vocab).filter_stop_words() for vocab in self.vocabs]
        self.model_manager = model_manager
        self.diff_from_prediction_score = abs(predicted_score - self.link.get_label())
        self.__analysis: JobAnalysis = None
        self.__link_analysis: LinkMetrics = None
        self._lock = Lock()

    def get_category_counts(self) -> Dict[str, int]:
        """
        Gets the counts of all analyzed words
        :return: A dictionary mapping analysis name and the result
        """
        analysis_counts = {}
        for analysis, result in self.get_analysis().items():
            n = result.total() if isinstance(result, WordCounter) else len(result)
            analysis_counts[analysis] = n
        return analysis_counts

    def get_link_info(self) -> LinkMetrics:
        """
        :return: Returns the link analysis.
        """
        if self.__link_analysis is None:
            analysis = self.get_analysis()
            for name, result in analysis.items():
                if isinstance(result, WordCounter):
                    analysis[name] = result.as_dict()
            self.__link_analysis = {
                self.ARTIFACT_TOKENS: [self.link.source.token, self.link.target.token],
                self.LINK_TRUE_LABEL: self.link.get_label(),
                self.ANALYSIS: analysis,
                self.DIFF_FROM_PREDICTION_SCORE: self.diff_from_prediction_score
            }
        return self.__link_analysis

    def get_analysis(self) -> Dict[str, Any]:
        """
        Gets the counts of all analyzed words
        :return: A dictionary mapping analysis name and the result
        """
        if self.__analysis is None:
            self.__analysis = {
                self.COMMON_WORDS: self.get_words_in_common(),
                self.MISSPELLED_WORDS: self.get_misspelled_words(),
            }
            self.__analysis[self.SHARED_SYNONYMS], self.__analysis[self.SHARED_ANTONYMS] = self.get_shared_synonyms_and_antonyms()
            self.__analysis[self.OOV_WORDS] = self.get_oov_words().difference(self.__analysis[self.MISSPELLED_WORDS])
        return self.__analysis

    def save(self, output_dir: str) -> str:
        """
        Saves the analysis output to the given directory
        :param output_dir: The directory to save to
        :return: The full filepath where the output was saved
        """
        output_file_path = os.path.join(output_dir, self.OUTPUT_FILENAME.format(str(self.link.id)))
        output_dict = self.get_link_info()
        FileUtil.write(output_dict, output_file_path)
        return output_file_path

    def get_words_in_common(self) -> Set[str]:
        """
        Gets the set of words that are shared between the two artifacts
        :return: The intersecting set of words
        """
        return self.word_counts[0].intersection(self.word_counts[1]).get_word_set()

    def get_misspelled_words(self) -> "WordCounter":
        """
        Gets the misspelled words from the artifacts
        :return: The list of misspelled words
        """
        misspelled = WordCounter()
        for word_count in self.word_counts:
            misspelled.update(word_count.get_misspelled_words())
        return misspelled

    def get_oov_words(self) -> "WordCounter":
        """
        Gets all the OOV words from the artifacts
        :return The set of OOV words
        """
        if not self.model_manager:
            return WordCounter()
        oov_words = WordCounter()
        for word_count in self.word_counts:
            oov_words.update(word_count.get_oov_words(self.model_manager))
        return oov_words

    def get_shared_synonyms_and_antonyms(self) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
        """
        Gets the synonyms from the vocab
        :return: A set of synonyms for the vocab
        """

        def add_related_word_if_shared(related_word: str, shared_dict: Dict):
            if related_word in self.word_counts[1]:
                if orig_word not in shared_dict:
                    shared_dict[orig_word] = set()
                shared_dict[orig_word].add(related_word)

        shared_synonyms, shared_antonyms = {}, {}
        for orig_word in self.word_counts[0]:
            for synset in wn.synsets(orig_word):
                if synset is None:
                    continue
                for lemma in synset.lemmas():
                    if lemma.name() != orig_word and lemma.name():
                        add_related_word_if_shared(lemma.name(), shared_synonyms)
                    for antonym in lemma.antonyms():
                        add_related_word_if_shared(antonym.name(), shared_antonyms)
        return shared_synonyms, shared_antonyms

    @staticmethod
    def get_artifact_vocab(artifact: Artifact) -> List[str]:
        """
        Gets the vocabulary of the artifact
        :param artifact: The artifact to get vocab of
        :return: The vocabulary of the artifact
        """
        artifact_body = word_tools.CLEANER.run([artifact.token.lower()]).pop()
        return artifact_body.split()
