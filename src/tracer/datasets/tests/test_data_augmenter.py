from test.base_test import BaseTest
from tracer.datasets.data_augmenter import DataAugmenter


class TestDataAugmenter(BaseTest):

    def test_run(self):
        # TODO
        pass

    def get_data_augmenter(self):
        return DataAugmenter(0.15)
