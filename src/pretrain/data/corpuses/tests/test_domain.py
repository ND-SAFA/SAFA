from django.test import TestCase

from common.config.paths import PROJ_PATH
from pretrain.data.corpuses.domain import get_path, Domain
import os


class TestDomain(TestCase):
    EXPECTED_PATH = os.path.join(PROJ_PATH, "pretrain", "data", "corpuses", "base")

    def test_get_path(self):
        path = get_path(Domain.BASE)
        self.assertEquals(self.EXPECTED_PATH, path)
