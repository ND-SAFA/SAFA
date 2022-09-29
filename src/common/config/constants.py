# -------------- MODELS --------------
import os

LOGITS = "logits"
LOSS = "loss"

# -------------- MODELS --------------
IS_TEST = os.getenv("DEPLOYMENT", "development").lower() == "test"
DELETE_TEST_OUTPUT = os.getenv("DELETE_TEST_OUTPUT", "true") == "true"
MNT_DIR = os.environ.get('MNT_DIR', "")
