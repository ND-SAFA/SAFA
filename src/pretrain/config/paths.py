from os.path import dirname, join, abspath

PRETRAIN_PATH = dirname(dirname(abspath(__file__)))
DATA_PATH = join(PRETRAIN_PATH, "data")
CORPUS_DIR = join(DATA_PATH, "corpuses")
ELECTRA_PATH = join(PRETRAIN_PATH, "electra")
