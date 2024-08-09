from typing import Dict, List, Optional, Union

from common_resources.data.tdatasets.idataset import iDataset
from common_resources.tools.util.base_object import BaseObject
from common_resources.tools.experiment_serializer import ExperimentSerializer
from common_resources.tools.util.reflection_util import ReflectionUtil
from common_resources_test.base_tests.base_test import BaseTest
from common_resources.tools.variables.definition_variable import DefinitionVariable
from common_resources.tools.variables.experimental_variable import ExperimentalVariable
from common_resources.tools.variables.variable import Variable
from common_resources_test.test_object_definitions import TestObjectDefinitions


class TestWithOptional(BaseObject):
    def __init__(self, a: Optional[float] = None):
        self.a = a


class TestClass(BaseObject):
    def __init__(self, a: str, b: int, c: float, d: List[str]):
        self.a = a
        self.b = b
        self.c = c
        self.d = d


class TestOuterClass(BaseObject):
    def __init__(self, a: TestClass):
        self.a = a


class TestBaseObject(BaseTest):
    class_params = {
        "a": "helloworld",
        "b": 42,
        "c": 4.2,
        "d": ["hello", "world"]
    }

    def test_get_param_specs(self):
        param_variables = {param_name: Variable(param_value) for param_name, param_value in
                           self.class_params.items()}
        definition_variable = DefinitionVariable(param_variables)
        test_class = TestClass.initialize_from_definition(definition_variable)
        self.assert_has_params(test_class, self.class_params)

    def test_get_param_spects_invalid(self):
        invalid_param_tests = [("a", 42), ("b", "wrongtype",), ("c", [42]), ("d", "single")]
        for param_name, invalid_value in invalid_param_tests:
            invalid_params = self.class_params.copy()
            invalid_params[param_name] = invalid_value
            param_variables = {param_name: Variable(param_value) for param_name, param_value in invalid_params.items()}
            definition_variable = DefinitionVariable(param_variables)

            def create():
                test_class = TestClass.initialize_from_definition(definition_variable)

            self.assertRaises(TypeError, create, "Failed: " + param_name)

    def test_nested_specs(self):
        nested_params = {
            "definition": {
                "a": self.class_params
            }
        }
        definition_variable = ExperimentSerializer.create(nested_params)
        outer_class = TestOuterClass.initialize_from_definition(definition_variable)
        self.assert_has_params(outer_class.a, self.class_params)

    def test_optional_valid(self):
        valid_values = [None, 4.2]
        for value in valid_values:
            definition: Dict = {
                "a": value
            }
            object = TestObjectDefinitions.create(TestWithOptional, override=True, **definition)
            self.assert_has_params(object, definition)

    def test_optional_invalid(self):
        definition: Dict = {
            "a": "invalid-value"
        }

        with self.assertRaises(TypeError) as e:
            TestObjectDefinitions.create(TestWithOptional, override=True, **definition)

    def test_invalid_child_object(self):
        definition = {
            "a": {
                "a": 4.2
            }
        }

        def create():
            TestObjectDefinitions.create(TestOuterClass, override=True, **definition)

        self.assertRaises(TypeError, create)

    def test_optional_lists(self):
        value = ExperimentalVariable([Variable("a"), Variable("b")])
        target_type = Union[List[iDataset], ExperimentalVariable]
        BaseObject._assert_type(value, target_type, "test_param")

    def assert_has_params(self, instance, params):
        for param_name, param_value in params.items():
            class_value = getattr(instance, param_name)
            self.assertEqual(param_value, class_value)

    def test_get_base_class(self):
        optional_param = BaseObject._get_base_class(Optional[iDataset])
        nested_list_param = BaseObject._get_base_class(List[List[iDataset]])
        base_object_param = BaseObject._get_base_class(iDataset)

        for param in [optional_param, nested_list_param, base_object_param]:
            self.assertTrue(ReflectionUtil.is_instance_or_subclass(param, iDataset))
