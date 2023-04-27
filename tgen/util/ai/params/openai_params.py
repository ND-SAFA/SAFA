from tgen.train.trainers.trainer_task import TrainerTask


class OpenAiParams:
    """
    Contains possible parameters to OpenAI API.
    """
    COMPUTE_CLASSIFICATION_METRICS = "compute_classification_metrics"
    MODEL_SUFFIX = "model_suffix"
    N_EPOCHS = "n_epochs"
    LEARNING_RATE_MULTIPLIER = "learning_rate_multiplier"
    TEMPERATURE = "temperature"
    MAX_TOKENS = "max_tokens"
    LOG_PROBS = "logprobs"
    PROMPT = "prompt"
    VALIDATION_FILE = "validation_file"
    CLASSIFICATION_POSITIVE_CLASS = "classification_positive_class"

    EXPECTED_PARAMS_FOR_TASK = {TrainerTask.CLASSIFICATION: [COMPUTE_CLASSIFICATION_METRICS],
                                TrainerTask.TRAIN: [MODEL_SUFFIX, N_EPOCHS,
                                                    LEARNING_RATE_MULTIPLIER],
                                TrainerTask.PREDICT: [TEMPERATURE, MAX_TOKENS, LOG_PROBS]}
