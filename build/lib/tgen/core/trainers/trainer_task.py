from common_resources.tools.util.supported_enum import SupportedEnum


class TrainerTask(SupportedEnum):
    TRAIN = "fine-tune"
    PREDICT = "predict"
    SUMMARIZE = "summarize"
    PUSH = "push"
    PRE_TRAIN = "pre_train"
