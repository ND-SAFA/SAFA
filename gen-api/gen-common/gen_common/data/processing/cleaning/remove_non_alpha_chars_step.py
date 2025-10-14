from typing import List

from gen_common.data.processing.abstract_data_processing_step import AbstractDataProcessingStep


class RemoveNonAlphaCharsStep(AbstractDataProcessingStep):
    """
    Removes non-alpha numeric characters from strings.
    ---
    This is useful for removing code syntax.
    """

    def run(self, data_entries: List, **kwargs) -> List:
        """
        Returns entries with non-alpha numeric words removed.
        :param data_entries: The data entries being cleaned.
        :param kwargs: Additional arguments, currently ignored.
        :return:
        """
        result = [RemoveNonAlphaCharsStep.remove_non_alphanumeric_characters(s) for s in data_entries]
        return result

    @staticmethod
    def remove_non_alphanumeric_characters(doc):
        """
        Filters through all characters in document and removed all non-alpha numeric ones.
        :param doc: The document to clean.
        :return: The document without alphanumeric characters.
        """
        return "".join(filter(RemoveNonAlphaCharsStep.is_alpha_or_space, doc))

    @staticmethod
    def is_alpha_or_space(letter: str):
        """
        Returns whether given letter is alpha or space characters.
        :param letter: The letter being checked.
        :return: True if alpha or space, false otherwise.
        """
        return str.isalpha(letter) or str.isspace(letter)
