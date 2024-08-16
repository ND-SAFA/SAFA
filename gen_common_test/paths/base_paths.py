import os
from os.path import abspath, dirname, join

TEST_DIR_PATH = dirname(dirname(abspath(__file__)))
TEST_DATA_DIR = join(TEST_DIR_PATH, "test_data")
TEST_VOCAB_FILE = join(TEST_DATA_DIR, "test_vocab.txt")
TEST_OUTPUT_DIR = join(TEST_DIR_PATH, "output")
PRETRAIN_DIR = join(TEST_DATA_DIR, "pre_train")
TEST_HGEN_PATH = join(TEST_DATA_DIR, "hgen")
TEST_STATE_PATH = join(TEST_DATA_DIR, "state")
#
TEST_RESULT_READER = join(TEST_DATA_DIR, "result_reader")
# github
GITHUB_REPO_DIR = join(TEST_DATA_DIR, "github")
GITHUB_REPO_ARTIFACTS_DIR = join(GITHUB_REPO_DIR, "artifacts")
# cleaning
TEST_FILE_PATH = os.path.join(TEST_DATA_DIR, "cleaning", "test.hpp")
TEST_JAVA_PATH = os.path.join(TEST_DATA_DIR, "cleaning", "test.java")
