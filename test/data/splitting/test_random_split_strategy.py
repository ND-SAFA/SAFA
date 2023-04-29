from tgen.data.splitting.supported_split_strategy import SupportedSplitStrategy
from tgen.testres.base_tests.base_split_test import BaseSplitTest


class TestRandomSplitStrategy(BaseSplitTest):
    """
    Responsible for testing that random splits contain
    the right proportion of links.
    """

    def test_split_sizes(self):
        split_type = SupportedSplitStrategy.SPLIT_BY_LINK
        self.assert_split_multiple(split_type)
