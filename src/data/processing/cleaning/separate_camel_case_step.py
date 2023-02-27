import re
from typing import List

from data.processing.abstract_data_processing_step import AbstractDataProcessingStep


class SeparateCamelCaseStep(AbstractDataProcessingStep):
    """
    Responsible for identifying camel case words and separating them into individual words.
    """

    def run(self, data_entries: List, **kwargs) -> List:
        """
        Separates camel case words in data entries.
        :param data_entries: The data entries to process.
        :param kwargs: Ignored.
        :return: Processed data entries.
        """
        pass

    @staticmethod
    def separate_camel_case(doc: str):
        """
        Finds words written in camel casing and separates them into individual words.
        :param doc: The document to split camel case words.
        :return: Processed document.
        """
        split_doc = re.sub("([A-Z][a-z]+)", r" \1", re.sub("([A-Z]+)", r" \1", doc)).split()
        return " ".join(split_doc)
