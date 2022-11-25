from enum import Enum

from tracer.datasets.processing.augmentation.simple_word_replacement_step import SimpleWordReplacementStep


class AugmentationStep(Enum):
    SIMPLE_WORD_REPLACEMENT = SimpleWordReplacementStep

    def get_step_attributes(self):
        for step_class in AugmentationStep:
            step_attributes = dir(step_class)
