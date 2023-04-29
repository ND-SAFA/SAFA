from typing import List

from tqdm import tqdm

from tgen.data.processing.abstract_data_processing_step import AbstractDataProcessingStep
from tgen.data.processing.abstract_data_processor import AbstractDataProcessor


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
