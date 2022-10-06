from typing import Dict, List

from common.pre_processing.pre_processing_options import PreProcessingOptions


class PreProcessor:

    ORDERED_STEPS = PreProcessingOptions.get_ordered_steps()

    def __init__(self, pre_process_options: Dict[PreProcessingOptions, bool]):
        self.pre_process_options = pre_process_options

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
            for step in self.ORDERED_STEPS:
                if self.pre_process_options.get(step.value, False):
                    word_list = step.value().run(word_list)
            processed_content.append(PreProcessor.reconstruct_content(word_list))
        return processed_content
