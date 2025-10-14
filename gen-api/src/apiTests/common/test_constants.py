import os

dir_path = os.path.dirname(__file__)
ROOT_PATH = os.path.normpath(os.path.join(dir_path, "..", "..", ".."))
API_DATA_PATH = os.path.join(ROOT_PATH, "data")

SOURCE_PATH = os.path.join(API_DATA_PATH, "sources")
SOURCE_CODE_PATH = os.path.join(SOURCE_PATH, "java.csv")
FR_ARTIFACT_PATH = os.path.join(SOURCE_PATH, "functional_requirements.csv")
SUMMARY_PATH = os.path.join(SOURCE_PATH, "project_summary.txt")
SUMMARY_JSON_PATH = os.path.join(SOURCE_PATH, "project_summary.json")
CHILD_TYPE = "Java"
PARENT_TYPE = "Functional Requirement"
