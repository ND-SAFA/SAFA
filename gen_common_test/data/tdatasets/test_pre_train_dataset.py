from gen_common.data.tdatasets.pre_train_dataset import PreTrainDataset
from gen_common_test.base.tests.base_test import BaseTest
from gen_common_test.paths.base_paths import TEST_VOCAB_FILE


class TestPreTrainDataset(BaseTest):

    def get_pre_train_dataset(self):
        return PreTrainDataset(TEST_VOCAB_FILE, block_size=128)
