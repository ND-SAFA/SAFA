from typing import Dict

from tracer.pre_processing.pre_processing_steps import PreProcessingSteps


class PreProcessingStepContainer:
    def __init__(self, step: PreProcessingSteps, params: Dict):
        self.step = step
        self.params = params
