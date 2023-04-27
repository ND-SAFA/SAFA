from tgen.util.supported_enum import SupportedEnum


class TrainerTask(SupportedEnum):
    CLASSIFICATION = "classification"  # used internally only
    TRAIN = "fine-tune"
    PREDICT = "predict"
    SUMMARIZE = "summarize"
    PUSH = "push"
    PRE_TRAIN = "pre_train"
