from typing import Dict, List, Optional, Union

from jobs.abstract_job import AbstractJob
from server.serializers.experiment_serializer import ExperimentSerializer
from test.base_test import BaseTest
from test.test_object_creator import TestObjectCreator
from util.base_object import BaseObject
from util.variables.definition_variable import DefinitionVariable
from util.variables.experimental_variable import ExperimentalVariable
from util.variables.variable import Variable


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
        experiment_serializer = ExperimentSerializer(data=nested_params)
        assert experiment_serializer.is_valid(), experiment_serializer.errors
        definition_variable = experiment_serializer.save()
        print(definition_variable)
        outer_class = TestOuterClass.initialize_from_definition(definition_variable)
        self.assert_has_params(outer_class.a, self.class_params)

    def test_optional_valid(self):
        valid_values = [None, 4.2]
        for value in valid_values:
            definition: Dict = {
                "a": value
            }
            object = TestObjectCreator.create(TestWithOptional, override=True, **definition)
            self.assert_has_params(object, definition)

    def test_optional_invalid(self):
        definition: Dict = {
            "a": "invalid-value"
        }

        def create():
            object = TestObjectCreator.create(TestWithOptional, override=True, **definition)

        self.assertRaises(TypeError, create)

    def test_invalid_child_object(self):
        definition = {
            "a": {
                "a": 4.2
            }
        }

        def create():
            TestObjectCreator.create(TestOuterClass, override=True, **definition)

        self.assertRaises(TypeError, create)

    def test_optional_lists(self):
        value = ExperimentalVariable([Variable("a"), Variable("b")])
        target_type = Union[List[AbstractJob], ExperimentalVariable]
        BaseObject._assert_type(value, target_type, "test_param")

    def assert_has_params(self, instance, params):
        for param_name, param_value in params.items():
            class_value = getattr(instance, param_name)
            self.assertEqual(param_value, class_value)
