from tgen.train.trainers.trainer_task import TrainerTask


class AnthropicParams:
    """
    Contains allowed parameters to anthropic API.
    """
    PROMPT = "prompt"
    MODEL = "model"  # claude-v1, claude-v1.2, claude-v1.3, claude-instant-v1, claude-instant-v1.0
    MAX_TOKENS_TO_SAMPLE = "max_tokens_to_sample"
    STOP_SEQUENCES = "stop_sequences"
    STREAM = "stream"
    TEMPERATURE = "temperature"
    TOP_K = "top_k"
    top_p = "top_p"

    EXPECTED_PARAMS_FOR_TASK = {TrainerTask.CLASSIFICATION: [],
                                TrainerTask.TRAIN: [MODEL],
                                TrainerTask.PREDICT: [TEMPERATURE, MAX_TOKENS_TO_SAMPLE]}
