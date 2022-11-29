from enum import Enum
from typing import Dict

from server.serializers.dataset.dataset_creator_serializer import ParamScope
from test.base_test import BaseTest
from util import ReflectionUtil


class TestClassOne:
    def __init__(self):
        self.local = "local"
        self._protected = "protected"
        self.__private = "private"


class TestClassTwo:
    def __init__(self):
        self.local = "local"
        self._protected = "protected"
        self.__private = "private"


class TestEnum(Enum):
    ONE = TestClassOne
    TWO = TestClassTwo


class TestReflectionUtil(BaseTest):

    def test_get_param_scope(self):
        self.__assert_scope("hello", ParamScope.LOCAL)
        self.__assert_scope("_hello", ParamScope.PROTECTED)
        self.__assert_scope("__hello", ParamScope.PRIVATE)
        self.__assert_scope("_TestClass__hello", ParamScope.PRIVATE, "TestClass")

    def test_get_fields(self):
        scopes = [(ParamScope.LOCAL, {"local": "local"}),
                  (ParamScope.PROTECTED, {"_protected": "protected"}),
                  (ParamScope.PRIVATE, {"_TestClassOne__private": "private"})]
        test_class = TestClassOne()
        expected_fields = {}

        for scope, scope_fields in scopes:
            expected_fields.update(scope_fields)
            self.__test_fields(test_class, scope, expected_fields)

    def test_get_enum_key(self):
        tests = [(TestClassOne(), "ONE"), (TestClassTwo(), "TWO")]
        for test_class, key_name in tests:
            enum_key = ReflectionUtil.get_enum_key(TestEnum, test_class)
            self.assertEqual(key_name, enum_key)

    def test_set_attributes(self):
        test_class = TestClassOne()
        expected_value = "hello"
        ReflectionUtil.set_attributes(test_class, {"local": expected_value})
        self.assertEqual(test_class.local, expected_value)

    def __assert_scope(self, param_name, expected_scope: ParamScope, class_name: str = None):
        param_scope = ReflectionUtil.get_field_scope(param_name, class_name=class_name)
        self.assertEqual(param_scope, expected_scope)

    def __test_fields(self, instance, param_scope: ParamScope, expected_fields: Dict):
        fields = ReflectionUtil.get_fields(instance, param_scope)
        for field_name, field_value in expected_fields.items():
            self.assertIn(field_name, fields)
            self.assertEqual(field_value, fields[field_name])
