from enum import Enum


class RunMode(Enum):
    PUSH = "push"
    LEARNING_MODEL = "lm"
    TRAIN = "train"
    EVAL = "eval"
    TRAINEVAL = "traineval"
