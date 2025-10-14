from typing import Callable, List, Optional

from gen_common.infra.base_object import BaseObject
from gen_common_test.base.tests.base_test import BaseTest


class Parent:
    pass


class Child(Parent):
    pass


class TestIsInstance(BaseTest):

    def test_primitives(self):
        self.positive_test(5, int)
        self.positive_test(5, float)
        self.negative_test(5, str)

    def test_classes(self):
        p = Parent()
        c = Child()
        # Parent class
        self.negative_test(p, Child)
        self.positive_test(p, Parent)

        # Child Class
        self.positive_test(c, Parent)
        self.positive_test(c, Child)

    def test_lists(self):
        a: List[int] = [42]
        self.negative_test(a, List[str])
        self.positive_test(a, List[int])

    def test_functions(self):
        a: Callable[[str], str] = lambda s: s
        self.negative_test(a, List[str])
        self.positive_test(a, Callable[[str], str])
        self.positive_test(a, Callable)

    def test_optionals(self):
        a: Optional[str] = None
        self.negative_test(a, str)
        self.positive_test(a, Optional[str])

    @staticmethod
    def positive_test(value, expected_type):
        BaseObject._assert_type(value, expected_type, "test_param")

    def negative_test(self, value, expected_type):
        def try_parse():
            BaseObject._assert_type(value, expected_type, "test_param")

        self.assertRaises(TypeError, try_parse)
