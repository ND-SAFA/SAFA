from data.datasets.splitting.supported_split_strategy import SupportedSplitStrategy
from data.datasets.splitting.tests.base_split_test import BaseSplitTest


class TestCombinationSplitStrategy(BaseSplitTest):
    """
    Test that combination split strategy produces correct split sizes and
    will reference all source artifacts.
    """

    def test_split_sizes(self):
        split_type = SupportedSplitStrategy.SPLIT_BY_SOURCE
        self.assert_split(split_type)
        self.assert_split_multiple(split_type)
