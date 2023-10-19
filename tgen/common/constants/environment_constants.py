import os

from dotenv import load_dotenv

load_dotenv()

IS_TEST = os.getenv("DEPLOYMENT", "development").lower() == "test"
DELETE_TEST_OUTPUT = os.getenv("DELETE_TEST_OUTPUT", "true").capitalize() == "True"
OPEN_AI_KEY = os.getenv("OPEN_AI_KEY", None)
OPEN_AI_ORG = os.getenv("OPEN_AI_ORG", None)
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", None)
