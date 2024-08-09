import os

from common_resources_test.paths.base_paths import TEST_DATA_DIR

REPO_PROJECT_PATH = os.path.join(TEST_DATA_DIR, "repo")
REPO_ONE_PROJECT_PATH = os.path.join(REPO_PROJECT_PATH, "one")
REPO_TWO_PROJECT_PATH = os.path.join(REPO_PROJECT_PATH, "two")
STRUCTURE_PROJECT_PATH = os.path.join(TEST_DATA_DIR, "structure")
CSV_PROJECT_PATH = os.path.join(TEST_DATA_DIR, "csv", "test_csv_data.csv")
SAFA_PROJECT_PATH = os.path.join(TEST_DATA_DIR, "safa")
PRE_TRAIN_TRACE_PATH = os.path.join(TEST_DATA_DIR, "pre_train_trace", "handbook.txt")
DATAFRAME_PROJECT_PATH = os.path.join(TEST_DATA_DIR, "dataframe")