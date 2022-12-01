from test.base_test import BaseTest
from data.data_key import DataKey


class TestDataKey(BaseTest):

    def test_get_feature_entry_keys(self):
        expected_keys = ["input_ids", "token_type_ids", "attention_mask"]
        feature_entry_keys = DataKey.get_feature_entry_keys()
        self.assertEquals(feature_entry_keys, expected_keys)
