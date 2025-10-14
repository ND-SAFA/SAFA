import os
import sys

REPO_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..")
REPO_PATH = os.path.normpath(REPO_PATH)
REPO_PATH = os.path.abspath(REPO_PATH)

API_PATH = os.path.join(REPO_PATH, "src")
TGEN_PATH = os.path.join(REPO_PATH, "tgen")


def load_source_code_paths() -> None:
    """
    Loads both API and TGEN onto the path.
    :return: None
    """
    if TGEN_PATH not in sys.path:
        sys.path.append(TGEN_PATH)
    if API_PATH not in sys.path:
        sys.path.append(API_PATH)
