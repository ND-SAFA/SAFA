from common_resources.data.tdatasets.pre_train_dataset import PreTrainDataset
from common_resources_test.base_tests.base_test import BaseTest
from common_resources_test.paths.base_paths import TEST_VOCAB_FILE


class TestPreTrainDataset(BaseTest):

    def get_pre_train_dataset(self):
        return PreTrainDataset(TEST_VOCAB_FILE, block_size=128)
