from dotenv import load_dotenv

load_dotenv()
OPENAI_MAX_THREADS = 1
OPENAI_MAX_ATTEMPTS = 3
TEMPERATURE_DEFAULT = 0.0
MAX_TOKENS_DEFAULT = 2000
MAX_TOKENS_BUFFER = 600
MAX_CHARS_BUFFER = 1000
LOGPROBS_DEFAULT = 2
LEARNING_RATE_MULTIPLIER_DEFAULT = None
COMPUTE_CLASSIFICATION_METRICS_DEFAULT = True
OPEN_AI_MODEL_DEFAULT = "gpt-4"
TOKENS_2_WORDS_CONVERSION = (3 / 4)  # open ai's rule of thumb for approximating tokens from number of words
TOKENS_2_CHARS_CONVERSION = (1 / 4)  # open ai's rule of thumb for approximating tokens from number of chars
