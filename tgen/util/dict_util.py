from typing import Dict, List, Iterable, Set

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

    @staticmethod
    def combine_child_dicts(parent: Dict, keys2combine: Iterable) -> Dict:
        """
        Combines the child dictionaries into a single dictionary
        :param parent: The parent dictionary containing the children to combine
        :param keys2combine: The keys of the children to combine
        :return: The dictionary containing the combination of children
        """
        combined = {}
        for key in keys2combine:
            combined.update(parent[key])
        return combined

    @staticmethod
    def filter_dict_keys(dict_: Dict, keys2keep: Set = None, keys2filter: Set = None) -> Dict:
        """
        Filters out keys in the dictionary
        :param dict_: The dictionary to filter
        :param keys2keep: The keys that should be kept
        :param keys2filter: The keys that should be filtered out
        :return: The filtered dictionary
        """
        if not keys2filter and not keys2keep:
            return dict_
        keys2filter = set(dict_.keys()).difference(keys2keep) if not keys2filter else keys2filter
        output_dict = {}
        for key in dict_.keys():
            if key not in keys2filter:
                output_dict[key] = dict_[key]
        return output_dict
