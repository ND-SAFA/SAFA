import re
from typing import List

from tgen.common.constants.deliminator_constants import SPACE
from tgen.common.util.str_util import StrUtil
from tgen.data.processing.abstract_data_processing_step import AbstractDataProcessingStep


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
        return [StrUtil.separate_camel_case(s) for s in data_entries]


