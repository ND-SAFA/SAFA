from scripts.results.script_definition import ScriptDefinition
from testres.base_test import BaseTest


class TestScriptDefinition(BaseTest):
    """
    Tests the pre-processing functions of a script definition.
    """

    def test_replace_object_property(self):
        """
        Tests that replacing object properties works for nested objects and lists.
        """
        data = {"list": [{"a": {"prop": 42}}], "other": {"a": {"prop": 42}}}
        expected_data = {"list": [{"a": {"prop": 4.2}}], "other": {"a": {"prop": 4.2}}}
        object_properties = ("a", "prop", 4.2)
        resulting_data = ScriptDefinition.set_object_property(object_properties, data)
        self.assertDictEqual(expected_data, resulting_data)
