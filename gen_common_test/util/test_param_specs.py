from gen_common.util import ParamSpecs
from gen_common_test.base_tests.base_test import BaseTest


class TestClassOne:
    def __init__(self, a: int):
        self.a = a


class TestParamSpecs(BaseTest):
    class_specs = None

    def setUp(self):
        self.class_specs = ParamSpecs.create_from_method(TestClassOne.__init__)

    def test_construction(self):
        self.assertIn("a", self.class_specs.param_names)
        self.assertIn("a", self.class_specs.required_params)
        self.assertEqual(self.class_specs.param_types["a"], int)
        self.assertFalse(self.class_specs.has_kwargs)

    def test_missing_param(self):
        definition = {}
        with self.assertRaises(TypeError) as cm:
            self.class_specs.assert_definition(definition)
        exception = cm.exception
        self.assertIn("missing required argument", exception.args[0])

    def test_extra_param(self):
        definition = {
            "a": 4,
            "b": "c"
        }
        with self.assertRaises(TypeError) as cm:
            self.class_specs.assert_definition(definition)
        exception = cm.exception
        self.assertIn("received unexpected arguments", exception.args[0])
