# -------------- MODELS --------------
import os

LOGITS = "logits"
LOSS = "loss"

# -------------- MODELS --------------
IS_TEST = os.getenv("DEPLOYMENT", "development") == "test"
DELETE_TEST_OUTPUT = os.getenv("DELETE_TEST_OUTPUT", "true") == "true"
