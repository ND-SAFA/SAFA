from typing import List

from tqdm import tqdm

from gen_common.data.processing.abstract_data_processing_step import AbstractDataProcessingStep
from gen_common.data.processing.abstract_data_processor import AbstractDataProcessor
from gen_common.infra.t_logging.logger_manager import logger


class DataCleaner(AbstractDataProcessor):

    def run(self, tokens: List[str], **kwargs) -> List[str]:
        """
        Runs the selected-preprocessing steps on each artifact content
        :param tokens: a list of artifact content strings
        :return: list of processed artifact content strings
        """
        if len(self.ordered_steps) == 0:
            return tokens
        logger.info(f"Cleaning {len(tokens)} artifacts.")
        word_lists = [AbstractDataProcessingStep.get_word_list(content) for content in tokens]
        for step in self.ordered_steps:
            for i in tqdm(range(len(word_lists)), desc=f"Performing {step.__class__.__name__} step..."):
                word_list = word_lists[i]
                processed_word_list = step.run(word_list)
                word_lists[i] = processed_word_list
        result = [AbstractDataProcessingStep.reconstruct_content(word_list) for word_list in word_lists]
        return result
