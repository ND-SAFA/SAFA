from common_resources.data.tdatasets.pre_train_dataset import PreTrainDataset
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_VOCAB_FILE


class TestPreTrainDataset(BaseTest):

    def get_pre_train_dataset(self):
        return PreTrainDataset(TEST_VOCAB_FILE, block_size=128)
