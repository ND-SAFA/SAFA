from typing import List

from nltk import PorterStemmer

from gen_common.constants import SPACE
from gen_common.data.processing.abstract_data_processing_step import AbstractDataProcessingStep


class LemmatizeWordStep(AbstractDataProcessingStep):
    """
    Lemmatizes each word in documents.
    """

    def __init__(self):
        """
        Initializes stemmer and step.
        """
        super().__init__()
        self.ps = PorterStemmer()

    def run(self, data_entries: List, **kwargs) -> List:
        """
        Lemmatizes each word in each entry.
        :param data_entries: Lists of data entries.
        :param kwargs: Ignored.
        :return: Processed entries.
        """
        return [self.stem_doc(s) for s in data_entries]

    def stem_doc(self, doc):
        """
        Removes numbers, newlines, parenthesis, stems words, and makes them all lower case
        :param doc: {String} The uncleaned string.
        :return: {String} Cleaned string.
        """
        if doc is None:
            raise Exception("Received None as text document")
        return SPACE.join([self.ps.stem(word) for word in doc.split(SPACE)])
