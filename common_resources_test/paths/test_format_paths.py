import os

from common_resources_test.paths.base_paths import TEST_DATA_DIR

FORMAT_PATH = os.path.join(TEST_DATA_DIR, "formats")

# Formats
FOLDER_PROJECT_PATH = os.path.join(FORMAT_PATH, "folder")
CSV_ENTITY_PATH = os.path.join(FORMAT_PATH, "csv", "test_csv_data.csv")
JSON_ENTITY_PATH = os.path.join(FORMAT_PATH, "json", "data.json")
XML_ENTITY_PATH = os.path.join(FORMAT_PATH, "xml", "data.xml")
