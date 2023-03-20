from typing import List, Type

from tqdm import tqdm

from data.processing.abstract_data_processing_step import AbstractDataProcessingStep
from data.processing.abstract_data_processor import AbstractDataProcessor
from data.processing.cleaning.supported_data_cleaning_step import SupportedDataCleaningStep
from util.base_object import BaseObject
from util.override import overrides


class DataCleaner(AbstractDataProcessor):

    def run(self, tokens: List[str], **kwargs) -> List[str]:
        """
        Runs the selected-preprocessing steps on each artifact content
        :param tokens: a list of artifact content strings
        :return: list of processed artifact content strings
        """
        processed = []
        word_lists = [AbstractDataProcessingStep.get_word_list(content) for content in tokens]
        for word_list in tqdm(word_lists, desc="Cleaning artifacts..."):
            processed_word_list = word_list
            for step in self.ordered_steps:
                processed_word_list = step.run(processed_word_list)
            processed.append(processed_word_list)
        return [AbstractDataProcessingStep.reconstruct_content(word_list) for word_list in processed]

    @classmethod
    @overrides(BaseObject)
    def _get_child_enum_class(cls, abstract_class: Type, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
        :param abstract_class: the abstract parent class type
        :param child_class_name: the name of the child class
        :return: the enum class mapping name to class
        """
        return SupportedDataCleaningStep
