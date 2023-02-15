import os
from typing import Tuple, List, Dict, Any

import nltk
from readability.readability import Readability
from readability.exceptions import ReadabilityException

from analysis.link_analyzer import LinkAnalyzer
from analysis.word_tools import WordCounter
from constants import HIGH_FREQ_THRESHOLD_DEFAULT, LOW_FREQ_THRESHOLD_DEFAULT
from data.datasets.trace_dataset import TraceDataset
from models.model_manager import ModelManager
from util.file_util import FileUtil
from util.logging.logger_manager import logger

nltk.download('punkt', quiet=True)


class DatasetAnalyzer:
    """
    Handles analysis of a dataset
    """
    READABILITY_SCORE = "readability_score"
    HIGH_FREQUENCY_WORDS = "high_freq_words"
    LOW_FREQUENCY_WORDS = "low_freq_words"
    MISSPELLED_WORDS = "misspelled_words"
    OOV_WORDS = "oov_words_with_model_{}"

    OUTPUT_FILENAME = "dataset_analysis_output.json"

    def __init__(self, dataset: TraceDataset, model_managers: List[ModelManager]):
        """
        Initializes the analyzer for analysis of given dataset
        :param dataset: The dataset to from which OOV words will be extracted
        """
        self.dataset = dataset
        self.vocab = self._get_vocab()
        self.word_counts = WordCounter(self.vocab).filter_stop_words()
        self.model_managers = model_managers
        self.__analysis = None

    def get_analysis(self) -> Dict[str, Any]:
        """
        Gets the analysis of the dataset
        :return: A dictionary mapping analysis name to its result
        """
        if self.__analysis is None:
            self.__analysis = {
                self.READABILITY_SCORE: self.get_readability_score(),
                self.HIGH_FREQUENCY_WORDS: self.get_high_frequency_word_counts(),
                self.LOW_FREQUENCY_WORDS: self.get_low_frequency_word_counts(),
                self.MISSPELLED_WORDS: self.get_misspelled_words()
            }
            for model in self.model_managers:
                self.__analysis[self.OOV_WORDS.format(model.model_path)] = self.get_oov_words(model).difference(
                    self.__analysis[self.MISSPELLED_WORDS])
        return self.__analysis

    def analyze_and_save(self, output_dir: str) -> str:
        """
        Saves the analysis output to the given directory
        :param output_dir: The directory to save to
        :return: The output file path
        """
        analysis = self.get_analysis()
        output_file_path = os.path.join(output_dir, self.OUTPUT_FILENAME)
        FileUtil.write(analysis, output_file_path)
        return output_file_path

    def get_readability_score(self) -> float:
        """
        Gets the readability score of the dataset
        :return: The readability score and grade level of the dataset
        """
        try:
            r = Readability(" ".join(self.vocab))
            fk = r.flesch_kincaid()
            return fk.score
        except ReadabilityException as e:
            logger.warning("Unable to get readability score; %s" % e)
            return -1

    def get_high_frequency_word_counts(self, threshold: float = HIGH_FREQ_THRESHOLD_DEFAULT) -> Tuple[WordCounter, float]:
        """
        Determines words in the vocab that occur at a high frequency relative to the rest of the dataset
        :param threshold: Percentage of all vocab words, where all words that occur more than this amount will be considered high freq
        :return: A dictionary of high freq words and their counts and the proportion of high freq words to total vocab size
        """
        total_words = self.word_counts.total()
        high_frequency_counts = self.word_counts.filter(
            lambda _, count: count >= total_words * threshold)
        return high_frequency_counts, high_frequency_counts.total() / total_words

    def get_low_frequency_word_counts(self, threshold: float = LOW_FREQ_THRESHOLD_DEFAULT) -> Tuple[WordCounter, float]:
        """
        Determines words in the vocab that occur at a low frequency relative to the rest of the dataset
        :param threshold: Percentage of all vocab words, where all words that occur less than this amount will be considered low freq
        :return: A dictionary of low freq words and their counts and the proportion of low freq words to total vocab size
        """
        total_words = self.word_counts.total()
        low_frequency_counts = self.word_counts.filter(
            lambda _, count: count <= min(total_words * threshold, 1))
        return low_frequency_counts, low_frequency_counts.total() / total_words

    def get_misspelled_words(self) -> "WordCounter":
        """
        Gets the misspelled words from the dataset
        :return: The list of misspelled words
        """
        return self.word_counts.get_misspelled_words()

    def get_oov_words(self, model_manager: ModelManager) -> "WordCounter":
        """
        Gets all the OOV words from the dataset
        :param model_manager: The model to compare vocab to
        :return The set of OOV words
        """
        return self.word_counts.get_oov_words(model_manager)

    def _get_vocab(self) -> List[str]:
        """
        Gets all words in the dataset's artifact bodies
        :return: List of words from the datasets artifacts
        """
        artifact_ids = set()
        vocab = []
        for link in self.dataset.links.values():
            for artifact in [link.source, link.target]:
                if artifact.id in artifact_ids:
                    continue
                artifact_ids.add(artifact.id)
                vocab.extend(LinkAnalyzer.get_artifact_vocab(artifact))
        return vocab
