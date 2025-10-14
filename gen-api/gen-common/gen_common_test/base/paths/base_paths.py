from os.path import abspath, dirname, join

GEN_COMMON_TEST_DIR_PATH = dirname(dirname(dirname(abspath(__file__))))
GEN_COMMON_TEST_DATA_PATH = join(GEN_COMMON_TEST_DIR_PATH, "test_data")

GEN_COMMON_TEST_OUTPUT_PATH = join(GEN_COMMON_TEST_DIR_PATH, "output")
# Files
GEN_COMMON_TEST_TESTPYTHON_PATH = join(GEN_COMMON_TEST_DATA_PATH, "test_python.py")
GEN_COMMON_TEST_VOCAB_PATH = join(GEN_COMMON_TEST_DATA_PATH, "test_vocab.txt")
