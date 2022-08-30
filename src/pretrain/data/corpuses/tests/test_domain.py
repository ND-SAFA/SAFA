import os

from common.config.paths import PROJ_PATH
from pretrain.data.corpuses.domain import Domain, get_path
from test.base_test import BaseTest


class TestDomain(BaseTest):
    EXPECTED_PATH = os.path.join(PROJ_PATH, "pretrain", "data", "corpuses", "base")

    def test_get_path(self):
        path = get_path(Domain.BASE)
        self.assertEquals(self.EXPECTED_PATH, path)
