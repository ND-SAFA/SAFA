from os.path import dirname, abspath, join

TEST_DIR = dirname(dirname(abspath(__file__)))
TEST_VOCAB_FILE = join(TEST_DIR, "test_vocab.txt")
TEST_OUTPUT_DIR = join(TEST_DIR, "output")