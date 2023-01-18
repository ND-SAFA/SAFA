from testres.base_test import BaseTest
from util.json_util import JsonUtil


class TestJsonUtil(BaseTest):
    """
    Responsible for testing JSON utility methods
    """

    def test_get_property(self):
        """
        Tests ability to retrieve property in definition when present and catch error otherwise.
        """
        prop_name = "prop_name"
        prop_value = 1
        retrieved_value = JsonUtil.get_property({prop_name: prop_value}, prop_name)
        self.assertEqual(prop_value, retrieved_value)

    def test_get_property_default_value(self):
        """
        Tests ability to retrieve property in definition when present and catch error otherwise.
        """
        prop_name = "prop_name"
        default_value = 1
        retrieved_value = JsonUtil.get_property({}, prop_name, default_value)
        self.assertEqual(default_value, retrieved_value)

    def test_get_property_missing(self):
        """
        Tests ability to retrieve property in definition when present and catch error otherwise.
        """
        prop_name = "missing_prop_name"
        with self.assertRaises(ValueError) as e:
            JsonUtil.get_property({}, prop_name)
        error_message = " ".join(map(str, e.exception.args))
        self.assertIn(prop_name, error_message)
