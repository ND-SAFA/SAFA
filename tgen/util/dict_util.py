from typing import Dict, List

from tgen.util.list_util import ListUtil


class DictUtil:
    """
    Utility for pure operations on dictionary.
    """

    @staticmethod
    def assert_same_keys(links: List[Dict]) -> None:
        """
        Asserts that links are the same size and have the same keys.
        :param links: List of link mappings.
        :return: None
        """
        link_sizes = [len(l) for l in links]
        ListUtil.assert_mono_array(link_sizes)
        link_keys = [set(l.keys()) for l in links]
        for i in range(1, len(links)):
            before_keys = link_keys[i - 1]
            after_keys = link_keys[i]
            assert before_keys == after_keys, f"Expected {before_keys} to be equal to {after_keys}."

    @staticmethod
    def order(obj: Dict, properties: List[str]) -> Dict:
        """
        Sets the properties in dictionaries to come before the others.
        :param obj: The object to order.
        :param properties: The properties in the desired order.
        :return: Dictionary with new properties set in desired order.
        """
        defined = set(properties)
        obj_props = set(obj.keys())
        missing = obj_props.difference(defined)
        properties = properties + list(missing)
        return {k: obj[k] for k in properties}
