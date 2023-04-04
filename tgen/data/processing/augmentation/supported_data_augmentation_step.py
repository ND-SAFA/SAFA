from enum import Enum

from tgen.data.processing.augmentation.resample_step import ResampleStep
from tgen.data.processing.augmentation.simple_word_replacement_step import SimpleWordReplacementStep
from tgen.data.processing.augmentation.source_target_swap_step import SourceTargetSwapStep


class SupportedAugmentationStep(Enum):
    SIMPLE_WORD_REPLACEMENT = SimpleWordReplacementStep
    RESAMPLE = ResampleStep
    SOURCE_TARGET_SWAP = SourceTargetSwapStep
