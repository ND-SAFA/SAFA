from enum import Enum

from datasets.processing.augmentation.resample_step import ResampleStep
from datasets.processing.augmentation.simple_word_replacement_step import SimpleWordReplacementStep
from datasets.processing.augmentation.source_target_swap_step import SourceTargetSwapStep


class AugmentationStep(Enum):
    SIMPLE_WORD_REPLACEMENT = SimpleWordReplacementStep
    RESAMPLE = ResampleStep
    SOURCE_TARGET_SWAP = SourceTargetSwapStep

    def get_step_attributes(self):
        for step_class in AugmentationStep:
            step_attributes = dir(step_class)
