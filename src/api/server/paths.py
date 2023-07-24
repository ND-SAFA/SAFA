import os
import sys


def load_paths():
    REPO_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..")
    REPO_PATH = os.path.normpath(REPO_PATH)
    REPO_PATH = os.path.abspath(REPO_PATH)

    API_PATH = os.path.join(REPO_PATH, "src")
    TGEN_PATH = os.path.join(REPO_PATH, "tgen")
    modified = False
    if TGEN_PATH not in sys.path:
        sys.path.append(TGEN_PATH)
        modified = True
    if API_PATH not in sys.path:
        sys.path.append(API_PATH)
        modified = True
    if modified:
        print("PATHS:", sys.path)
