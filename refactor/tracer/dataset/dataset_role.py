from enum import Enum


class DatasetRole(Enum):
    PRE_TRAIN = "pre_train"
    TRAIN = "train"
    EVAL = "eval"
