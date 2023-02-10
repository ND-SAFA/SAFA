import string
from typing import Set

from data.datasets.trace_dataset import TraceDataset
from data.processing.cleaning.data_cleaner import DataCleaner
from data.processing.cleaning.remove_unwanted_chars_step import RemoveUnwantedCharsStep
from data.processing.cleaning.remove_white_space_step import RemoveWhiteSpaceStep
from data.processing.cleaning.separate_joined_words_step import SeparateJoinedWordsStep
from models.model_manager import ModelManager


class DatasetAnalyzer:
    """
    Handles analysis of a dataset
    """

    CLEANER = DataCleaner([RemoveWhiteSpaceStep(), SeparateJoinedWordsStep(),
                           RemoveUnwantedCharsStep(additional_unwanted_chars=string.punctuation + string.digits)])

    def __init__(self, dataset: TraceDataset):
        """
        Initializes the analyzer
        :param dataset: The dataset to from which OOV words will be extracted
        """
        self.dataset = dataset
        self.dataset_vocab = self.dataset.get_vocab(self.CLEANER)

    def get_oov_words(self, model_manager: ModelManager) -> Set[str]:
        """
        Gets all the OOV words from the dataset
        :param model_manager: The model whose vocab will be compared to the dataset
        :return The set of OOV words
        """
        model_vocab = model_manager.get_tokenizer().vocab.keys()
        return self.dataset_vocab.difference(model_vocab)
