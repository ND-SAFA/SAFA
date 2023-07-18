from dotenv import load_dotenv

load_dotenv()

TEMPERATURE_DEFAULT = 0.0
MAX_TOKENS_DEFAULT = 400
MAX_TOKENS_BUFFER = 400
LOGPROBS_DEFAULT = 2
LEARNING_RATE_MULTIPLIER_DEFAULT = None
COMPUTE_CLASSIFICATION_METRICS_DEFAULT = True
OPEN_AI_MODEL_DEFAULT = "gpt-3.5-turbo"
TOKENS_2_WORDS_CONVERSION = (3 / 4)  # open ai's rule of thumb for approximating tokens from number of words
