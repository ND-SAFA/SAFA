from enum import Enum


class TrainerTask(Enum):
    CLASSIFICATION = "classification"  # used internally only
    TRAIN = "fine-tune"
    PREDICT = "predict"
    SUMMARIZE = "summarize"
    PUSH = "push"
    PRE_TRAIN = "pre_train"
