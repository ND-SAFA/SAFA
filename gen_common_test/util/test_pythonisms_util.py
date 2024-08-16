from collections.abc import Set
from typing import Dict, List

from gen_common.util import default_mutable
from gen_common_test.base_tests.base_test import BaseTest


class TestPythonismsUtil(BaseTest):

    @default_mutable(allowed_none={"param4"})
    def fake_method(self, param1: int, param2: str, param3: Set[int] = None, param4: Dict[int, str] = None, param5: List = None):
        return param1, param2, param3, param4, param5

    @staticmethod
    @default_mutable()
    def fake_static_method(param1: int, param2: str, param3: Set[int] = None, param4: Dict[int, str] = None, param5: List = None):
        return param1, param2, param3, param4, param5

    def test_default_mutable_static(self):
        self.assert_default_mutable(*self.fake_static_method(1, "1"))

        set_defined = {1, 2, 3}
        params = self.fake_static_method(1, "1", set_defined)
        self.assert_default_mutable(*params)
        self.assertSetEqual(set_defined, params[2])

        params = self.fake_static_method(param1=1, param2="1", param5=list(set_defined))
        self.assert_default_mutable(*params)
        self.assertListEqual(list(set_defined), params[-1])

    def test_default_mutable(self):
        param5 = [1, 2, 3]
        params = self.fake_method(1, param2="1", param5=param5)
        self.assert_default_mutable(*params, allowed_to_be_none=True)
        self.assertListEqual(param5, params[-1])
        self.assertIsNone(params[3])

        param4 = {1: "1"}
        params = self.fake_method(1, param2="1", param4=param4)
        self.assert_default_mutable(*params, allowed_to_be_none=True)
        self.assertDictEqual(param4, params[3])

    def assert_default_mutable(self, param1, param2, param3, param4, param5, allowed_to_be_none: bool = False):
        self.assertIsInstance(param3, Set)
        if not allowed_to_be_none:
            self.assertIsInstance(param4, Dict)
        self.assertIsInstance(param5, List)
