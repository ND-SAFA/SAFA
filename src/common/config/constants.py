# -------------- MODELS --------------
import os

LOGITS = "logits"
LOSS = "loss"

# -------------- MODELS --------------
IS_TEST = os.getenv("DEPLOYMENT", "development") == "test"
