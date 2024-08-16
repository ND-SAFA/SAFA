import re
from typing import Dict, List

from gen_common.data.processing.abstract_data_processing_step import AbstractDataProcessingStep


class RegexReplacementStep(AbstractDataProcessingStep):
    """
    Performs a series of regex replacements on the documents.
    """

    def __init__(self, regex_replacements: Dict):
        """
        Initializes step with given replacements.
        :param regex_replacements: Set of regex replacements.
        """
        super().__init__()
        self.regex_replacements = regex_replacements

    def run(self, data_entries: List, **kwargs) -> List:
        """
        Performs the regex substitutions of data entries.
        :param data_entries: The entries to be processed.
        :param kwargs: Ignored
        :return: Processed entries.
        """
        processed_entries = []
        for entry in data_entries:
            for regex, replacement in self.regex_replacements.items():
                entry = re.sub(regex, replacement, entry).strip()
            processed_entries.append(entry)
        return processed_entries
