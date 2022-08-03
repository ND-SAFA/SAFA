from enum import IntEnum, auto


class JobType(IntEnum):
    PRETRAIN = auto()
    TRAIN = auto()
    EVALUATE = auto()
