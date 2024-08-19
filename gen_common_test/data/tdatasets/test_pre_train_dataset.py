from gen_common.data.tdatasets.pre_train_dataset import PreTrainDataset
from gen_common_test.base.paths.base_paths import GEN_COMMON_TEST_VOCAB_PATH
from gen_common_test.base.tests.base_test import BaseTest


class TestPreTrainDataset(BaseTest):

    def get_pre_train_dataset(self):
        return PreTrainDataset(GEN_COMMON_TEST_VOCAB_PATH, block_size=128)
