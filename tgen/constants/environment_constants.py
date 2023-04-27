import os
from dotenv import load_dotenv

load_dotenv()

IS_TEST = os.getenv("DEPLOYMENT", "development").lower() == "test"
DELETE_TEST_OUTPUT = os.getenv("DELETE_TEST_OUTPUT", "true").capitalize() == "True"
MNT_DIR = os.environ.get('MNT_DIR', "")