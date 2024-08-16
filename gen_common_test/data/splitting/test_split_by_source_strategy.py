from gen_common.data.splitting.supported_split_strategy import SupportedSplitStrategy
from gen_common_test.base_tests.base_split_test import BaseSplitTest


class TestRandomAllSourcesSplit(BaseSplitTest):
    """
    Responsible for testing that data splitting references all sources
    """

    def test_split_sizes(self):
        split_type = SupportedSplitStrategy.SPLIT_BY_SOURCE
        self.assert_split_multiple(split_type)
