import os

from dotenv.main import load_dotenv

load_dotenv()

USE_NL_SUMMARY_PROMPT = False
USE_NL_SUMMARY_EMBEDDINGS = os.getenv("USE_NL_SUMMARY_EMBEDDINGS", "False").lower() == "true"
