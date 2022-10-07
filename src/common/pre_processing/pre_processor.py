from typing import Dict, List

from common.pre_processing.pre_processing_options import PreProcessingOptions


class PreProcessor:

    def __init__(self, pre_process_options: Dict[PreProcessingOptions, bool],
                 word_replace_mappings: Dict[str, str] = None):
        self.pre_process_options = pre_process_options
        step_params = {PreProcessingOptions.REPLACE_WORDS: {"word_replace_mappings": word_replace_mappings}}
        self.ordered_steps = self.get_steps(step_params)

    def get_steps(self, step_params: Dict[PreProcessingOptions, Dict]):
        ordered_steps = []
        ordered_options = []
        for option in [step for step in PreProcessingOptions]:
            step = option.value(**step_params[option]) if option in step_params else option.value()
            ordered_steps.append(step)
            ordered_options.append(option)
        return sorted(zip(ordered_options, ordered_steps), key=lambda x: x[1])

    @staticmethod
    def get_word_list(content: str) -> List[str]:
        return list(filter(lambda w: len(w.strip()) > 0, content.replace("�", " ").split()))

    @staticmethod
    def reconstruct_content(word_list: List[str]) -> str:
        return " ".join(word_list)

    def run(self, artifact_content: List[str]) -> List[str]:
        processed_content = []
        for content in artifact_content:
            word_list = PreProcessor.get_word_list(content)
            for option, step in self.ordered_steps:
                if self.pre_process_options.get(option, False):
                    word_list = step.run(word_list)
            processed_content.append(PreProcessor.reconstruct_content(word_list))
        return processed_content
