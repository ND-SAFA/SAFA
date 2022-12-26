from os.path import abspath, dirname, join

TEST_DIR = dirname(dirname(abspath(__file__)))
TEST_DATA_DIR = join(TEST_DIR, "data")
TEST_VOCAB_FILE = join(TEST_DIR, "test_vocab.txt")
TEST_OUTPUT_DIR = join(TEST_DIR, "output")
PRETRAIN_DIR = join(TEST_DATA_DIR, "pre_train")
