from typing import List

from gen_common.constants.symbol_constants import PERIOD, SPACE
from gen_common.data.processing.abstract_data_processing_step import AbstractDataProcessingStep


class SplitChainedCallsStep(AbstractDataProcessingStep):
    """
    Splits chained code calls in documents.
    """

    def run(self, data_entries: List, **kwargs) -> List:
        """
        Removes chained call delimiters from data entries.
        :param data_entries: The data entries being processed.
        :param kwargs: Ignored.
        :return: Processed entries.
        """
        return [SplitChainedCallsStep.split_chained_calls(s) for s in data_entries]

    @staticmethod
    def split_chained_calls(doc, chained_call_delimiter=PERIOD, word_delimiter=SPACE):
        """
        Replaces chained called delimiter with space delimiter.
        :param doc: The document being processed.
        :param chained_call_delimiter: The delimiter separating chained calls.
        :param word_delimiter: The delimiter to replace chained called delimiter with.
        :return: Processed document.
        """
        return doc.replace(chained_call_delimiter, word_delimiter).strip()
