import string
from typing import Dict, Tuple, List
from analysis.supported_analysis import SupportedDatasetAnalysisSteps
from analysis.word_counter import WordCounter
from constants import HIGH_FREQ_THRESHOLD_DEFAULT, LOW_FREQ_THRESHOLD_DEFAULT
from data.datasets.trace_dataset import TraceDataset
from data.processing.cleaning.data_cleaner import DataCleaner
from data.processing.cleaning.remove_unwanted_chars_step import RemoveUnwantedCharsStep
from data.processing.cleaning.remove_white_space_step import RemoveWhiteSpaceStep
from data.processing.cleaning.separate_joined_words_step import SeparateJoinedWordsStep
from models.model_manager import ModelManager
from readability.readability import Readability
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)


class DatasetAnalyzer:
    """
    Handles analysis of a dataset
    """

    CLEANER = DataCleaner([RemoveWhiteSpaceStep(), SeparateJoinedWordsStep(),
                           RemoveUnwantedCharsStep(additional_unwanted_chars=string.punctuation + string.digits)])
    STOP_WORDS = set(stopwords.words('english'))

    def __init__(self, dataset: TraceDataset, analysis_steps: List[SupportedDatasetAnalysisSteps] = None):
        """
        Initializes the analyzer
        :param dataset: The dataset to from which OOV words will be extracted
        :param analysis_steps: The analysis steps to perform
        """
        self.dataset = dataset
        self.analysis_steps = SupportedDatasetAnalysisSteps.get_all() if analysis_steps is None else analysis_steps
        self.vocab = self._get_vocab()
        self.word_counts = WordCounter(self.vocab).filter(lambda word, _: word not in self.STOP_WORDS)
        self.__analysis = {}

    def get_readability_score(self) -> float:
        """
        Gets the readability score of the dataset
        :return: The readability score and grade level of the dataset
        """
        r = Readability(" ".join(self.vocab))
        fk = r.flesch_kincaid()
        return fk.score

    def get_high_frequency_word_counts(self, threshold: float = HIGH_FREQ_THRESHOLD_DEFAULT) -> Tuple[WordCounter, float]:
        """
        Determines words in the vocab that occur at a high frequency relative to the rest of the dataset
        :param threshold: Percentage of all vocab words, where all words that occur more than this amount will be considered high freq
        :return: A dictionary of high freq words and their counts and the proportion of high freq words to total vocab size
        """
        total_words = self.word_counts.total
        high_frequency_counts = self.word_counts.filter(
            lambda _, count: count >= total_words * threshold)
        return high_frequency_counts, high_frequency_counts.total / total_words

    def get_low_frequency_word_counts(self, threshold: float = LOW_FREQ_THRESHOLD_DEFAULT) -> Tuple[WordCounter, float]:
        """
        Determines words in the vocab that occur at a low frequency relative to the rest of the dataset
        :param threshold: Percentage of all vocab words, where all words that occur less than this amount will be considered low freq
        :return: A dictionary of low freq words and their counts and the proportion of low freq words to total vocab size
        """
        total_words = self.word_counts.total
        low_frequency_counts = self.word_counts.filter(
            lambda _, count: count <= min(total_words * threshold, 1))
        return low_frequency_counts, low_frequency_counts.total / total_words

    def get_oov_words(self, model_manager: ModelManager) -> WordCounter:
        """
        Gets all the OOV words from the dataset
        :param model_manager: The model whose vocab will be compared to the dataset
        :return The set of OOV words
        """
        model_vocab = model_manager.get_tokenizer().vocab.keys()
        dataset_vocab = set(self.word_counts.keys())
        oov_words = dataset_vocab.difference(model_vocab)
        return WordCounter.from_dict({word: self.word_counts[word] for word in oov_words})

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
                artifact_body = self.CLEANER.run([artifact.token.lower()]).pop()
                vocab.extend(artifact_body.split())
        return vocab
