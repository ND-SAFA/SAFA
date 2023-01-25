from data.splitting.supported_split_strategy import SupportedSplitStrategy
from data.splitting.tests.base_split_test import BaseSplitTest


class TestRandomSplitStrategy(BaseSplitTest):
    """
    Responsible for testing that random splits contain
    the right proportion of links.
    """

    def test_split_sizes(self):
        split_type = SupportedSplitStrategy.RANDOM
        self.assert_split(split_type)
        self.assert_split_multiple(split_type)
