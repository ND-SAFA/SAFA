from enum import Enum

from data.processing.augmentation.resample_step import ResampleStep
from data.processing.augmentation.simple_word_replacement_step import SimpleWordReplacementStep
from data.processing.augmentation.source_target_swap_step import SourceTargetSwapStep


class AugmentationStep(Enum):
    SIMPLE_WORD_REPLACEMENT = SimpleWordReplacementStep
    RESAMPLE = ResampleStep
    SOURCE_TARGET_SWAP = SourceTargetSwapStep
