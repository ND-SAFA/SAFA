from enum import Enum


class DatasetRole(Enum):
    PRE_TRAIN = "pre_train"
    VAL = "val"
    TRAIN = "train"
    EVAL = "eval"
