from abc import abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union

from common_resources.tools.util.reflection_util import ParamScope, ReflectionUtil
from common_resources_test.base_tests.base_test import BaseTest
from common_resources_test.test_constants import TEST_DIR_NAME
from common_resources_test.test_data.test_data_manager import TestDataManager


class TestClassOne:
    def __init__(self):
        self.local = "local"
        self._protected = "protected"
        self.__private = "private"

    def test_method(self):
        return

    @staticmethod
    def test_static_method():
        return

    @classmethod
    def test_class_method(cls):
        return

    @abstractmethod
    def test_abstract_method(self):
        return


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
        self.__assert_scope("hello", ParamScope.PUBLIC)
        self.__assert_scope("_hello", ParamScope.PROTECTED)
        self.__assert_scope("__hello", ParamScope.PRIVATE)
        self.__assert_scope("_TestClass__hello", ParamScope.PRIVATE, "TestClass")

    def test_get_fields(self):
        scopes = [(ParamScope.PUBLIC, {"local": "local"}),
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

    def test_is_type(self):
        self.assertTrue(ReflectionUtil.is_type([1], List[int], "name"))
        self.assertFalse(ReflectionUtil.is_type([1], List[str], "name"))

        self.assertTrue(ReflectionUtil.is_type(None, Optional[int], "name"))
        self.assertFalse(ReflectionUtil.is_type(None, str, "name"))

        self.assertTrue(ReflectionUtil.is_type({}, Union[Tuple[int, str], Dict], "name"))
        self.assertTrue(ReflectionUtil.is_type((1, "1"), Union[Tuple[int, str], Dict], "name"))
        self.assertFalse(ReflectionUtil.is_type((True, False), Union[Tuple[int, str], Dict], "name"))

    def test_get_cls_from_path(self):
        cls = ReflectionUtil.get_cls_from_path("common_resources.tools.util.reflection_util.ReflectionUtil")
        self.assertEqual(cls.__name__, ReflectionUtil.__name__)

        cls = ReflectionUtil.get_cls_from_path("bad.path")
        self.assertIsNone(cls)

        cls = ReflectionUtil.get_cls_from_path(f"{TEST_DIR_NAME}.test_data.test_data_manager.Keys")  # nested
        self.assertEqual(cls.__name__, TestDataManager.Keys.__name__)

    def test_is_a_function(self):
        self.assertTrue(ReflectionUtil.is_function(lambda x: x))
        self.assertTrue(ReflectionUtil.is_function(TestClassOne.test_method))
        self.assertTrue(ReflectionUtil.is_function(TestClassOne.test_class_method))
        self.assertTrue(ReflectionUtil.is_function(TestClassOne.test_static_method))
        self.assertTrue(ReflectionUtil.is_function(TestClassOne.test_abstract_method))
        self.assertFalse(ReflectionUtil.is_function(TestClassOne()))
        self.assertFalse(ReflectionUtil.is_function(TestClassOne))

    def test_get_obj_full_path(self):
        test_path = ReflectionUtil.get_obj_full_path(TestReflectionUtil.test_get_obj_full_path)
        self.assertIn(test_path, ['test_reflection_util.TestReflectionUtil.test_get_obj_full_path',
                                  'util.test_reflection_util.TestReflectionUtil.test_get_obj_full_path',
                                  f'{TEST_DIR_NAME}.util.test_reflection_util.TestReflectionUtil.test_get_obj_full_path'])

    def __assert_scope(self, param_name, expected_scope: ParamScope, class_name: str = None):
        param_scope = ReflectionUtil.get_field_scope(param_name, class_name=class_name)
        self.assertEqual(param_scope, expected_scope)

    def __test_fields(self, instance, param_scope: ParamScope, expected_fields: Dict):
        fields = ReflectionUtil.get_fields(instance, param_scope)
        for field_name, field_value in expected_fields.items():
            self.assertIn(field_name, fields)
            self.assertEqual(field_value, fields[field_name])
