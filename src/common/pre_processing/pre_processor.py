from typing import Dict, List

from common.pre_processing.pre_processing_options import PreProcessingOptions


class PreProcessor:
    ORDERED_OPTIONS = PreProcessingOptions.get_ordered_steps()

    def __init__(self, pre_process_options: Dict[PreProcessingOptions, bool], word_replace_mappings: Dict[str, str] = None):
        self.pre_process_options = pre_process_options
        step_params = {PreProcessingOptions.REPLACE_WORDS: {"word_replace_mappings": word_replace_mappings}}
        self.ordered_steps = self.get_steps(step_params)

    def get_steps(self, step_params: Dict[PreProcessingOptions, Dict]):
        ordered_steps = []
        for option in self.ORDERED_OPTIONS:
            step = option.value(**step_params[option]) if option in step_params else option.value()
            ordered_steps.append(step)
        return ordered_steps

    @staticmethod
    def get_word_list(content: str) -> List[str]:
        return content.split()

    @staticmethod
    def reconstruct_content(word_list: List[str]) -> str:
        return " ".join(word_list)

    def run(self, artifact_content: List[str]) -> List[str]:
        processed_content = []
        for content in artifact_content:
            word_list = PreProcessor.get_word_list(content)
            for step in self.ORDERED_OPTIONS:
                if self.pre_process_options.get(step.value, False):
                    word_list = step.value().run(word_list)
            processed_content.append(PreProcessor.reconstruct_content(word_list))
        return processed_content
