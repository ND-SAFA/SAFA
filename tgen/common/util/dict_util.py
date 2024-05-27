from enum import Enum
from typing import Any, Callable, Dict, Iterable, List, Set, Tuple, Type, TypeVar, Union

from tgen.common.util.enum_util import EnumDict
from tgen.common.util.list_util import ListUtil

T = TypeVar("T")


class DictUtil:
    """
    Utility for pure operations on dictionary.
    """

    @staticmethod
    def flip(dict_: Dict) -> Dict:
        """
        Flips the keys and values in the dictionary.
        :param dict_: Original dictionary.
        :return: Dictionary with keys and values flipped.
        """

        flipped_dict = {}

        def _add(key, val):
            """
            Adds the value to the flipped dict with key.
            :param key: The key to add to.
            :param val: The value to add.
            :return: None.
            """
            if key in flipped_dict:
                if isinstance(flipped_dict[key], list):
                    val = flipped_dict[key].append(val)
                else:
                    val = [flipped_dict[key], val]
            flipped_dict[key] = val

        for k, v in dict_.items():
            if isinstance(v, set) or isinstance(v, list):
                for child_val in v:
                    _add(child_val, k)
            else:
                _add(v, k)
        if any(isinstance(v, list) for v in flipped_dict.values()):  # ensure all value are same type
            flipped_dict = {k: (v if isinstance(v, list) else [v]) for k, v in flipped_dict.items()}
        return flipped_dict

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

    @staticmethod
    def create_trace_enum(obj: Type[T], enum_type: Type[Enum]) -> EnumDict:
        """
        Create enum dictionary from object.
        :param obj: The trace entry whose properties are extracted.
        :param enum_type: The properties to extract if they exist.
        :return: EnumDict containing keys found.
        """

        trace_keys = [key for key in enum_type if key.value in obj]
        return EnumDict({k: obj[k.value] for k in trace_keys})

    @staticmethod
    def convert_iterables_to_lists(obj: Union[Dict, List, Tuple]):
        """
        Converts any iterables to to lists.
        :param obj: The object whose values are converted to lists.
        :return:
        """
        if isinstance(obj, list) or isinstance(obj, tuple):
            return [DictUtil.convert_iterables_to_lists(i) for i in obj]
        elif isinstance(obj, dict):
            new_dict = {}
            for k, v in obj.items():
                new_dict[k] = DictUtil.convert_iterables_to_lists(v)
            return new_dict
        else:
            return obj

    @staticmethod
    def joining(list_of_dicts: List[Dict]) -> Dict:
        """
        Aggregates the values of dictionaries.
        :param list_of_dicts: The list of dictionaries to overlap.
        :return: Single dictionary with aggregated values.
        """
        global_dict = {}

        for d in list_of_dicts:
            for k, v in d.items():
                if k in global_dict:
                    global_dict[k] += v
                else:
                    global_dict[k] = v

        return global_dict

    @staticmethod
    def get_kwarg_values(kwargs: Dict, pop: bool = False, **keys) -> Any:
        """
        Gets all kwargs values for the given keys
        :param kwargs: The kwargs to get values from
        :param pop: If True, removes the values from the kwargs
        :param keys: The keys to retrieve from the kwargs along with a default value
        :return: Return the value for each key
        """
        if not keys:
            return
        values = []
        for key, default in keys.items():
            value = kwargs.get(key, default)
            values.append(value)
            if pop and key in kwargs:
                kwargs.pop(key)
        return values[0] if len(values) == 1 else values

    @staticmethod
    def update_kwarg_values(orig_kwargs: Dict, replace_existing: bool = True, **new_kwargs) -> Dict:
        """
        Gets all kwargs values for the given keys
        :param orig_kwargs: The kwargs to add to
        :param new_kwargs: Additional kwargs to add
        :param replace_existing: If True, overwrites an existing kwargs if it exists in the new kwargs
        :return: The updated kwargs
        """
        for key, val in new_kwargs.items():
            if replace_existing or key not in orig_kwargs:
                orig_kwargs[key] = val
        return orig_kwargs

    @staticmethod
    def initialize_value_if_not_in_dict(mapping: Dict, item_key: Any, value: Any) -> bool:
        """
        Sets the value of the key if it is not in the mapping.
        :param mapping: The mapping to add the value to.
        :param item_key: The key to set.
        :param value: The value to set the key to.
        :return: True if the item did not exist so was initialized else False
        """
        if item_key not in mapping:
            mapping[item_key] = value
            return True
        return False

    @staticmethod
    def set_or_increment_count(mapping: Dict, item_key: Any, increment_value: int = 1) -> None:
        """
        Adds item to mapping if it does not exists, otherwise increments it.
        :param mapping: The map to add item to.
        :param item_key: The key to store item under.
        :param increment_value: The value to increment the count by if the key is in the dict.
        :return: None
        """
        was_initialized = DictUtil.initialize_value_if_not_in_dict(mapping, item_key, increment_value)
        if not was_initialized:
            mapping[item_key] += increment_value

    @staticmethod
    def set_or_append_item(mapping: Dict, item_key: Any, item_value: Any, iterable_type: Type[Iterable] = list) -> None:
        """
        Initializes a list/set to mapping if it does not exists, and appends item either way.
        :param mapping: The map to add item to.
        :param item_key: The key to store item under.
        :param item_value: The value to append to list/set under key
        :param iterable_type: The type of iterable to use for the value
        :return: None
        """
        DictUtil.initialize_value_if_not_in_dict(mapping, item_key, iterable_type())
        if isinstance(item_value, iterable_type):
            for item in item_value:
                DictUtil.set_or_append_item(mapping, item_key, item, iterable_type)
            return

        if isinstance(mapping[item_key], set):
            mapping[item_key].add(item_value)
        elif isinstance(mapping[item_key], dict):
            child_key, child_value = item_value
            mapping[item_key][child_key] = child_value
        else:
            mapping[item_key].append(item_value)

    @staticmethod
    def get_missing_keys(obj: Dict, keys: List[str]) -> List[str]:
        """
        Extracts keys missing in dict.
        :param obj: Dictionary to check for keys.
        :param keys: The keys expected to be dictionary.
        :return: The missing keys.
        """
        missing_keys = [k for k in keys if k not in obj]
        return missing_keys

    @classmethod
    def contains_keys(cls, obj: Dict, keys: List[str]) -> bool:
        """
        Returns true if object contains all keys otherwise false.
        :param obj: The object to check for keys.
        :param keys: The keys to ensure in object.
        :return: True if keys present in obj.
        """
        missing_keys = cls.get_missing_keys(obj, keys)
        return len(missing_keys) == 0

    @staticmethod
    def get_key_by_index(dict_: Dict, index: int = 0) -> Any:
        """
        Gets the first key from the dictionary.
        :param dict_: The dictionary to get first key of.
        :param index: The index of the key to get.
        :return: The first key from the dictionary.
        """
        if len(dict_) == 0:
            return
        return list(dict_.keys())[index]

    @staticmethod
    def get_value_by_index(dict_: Dict, index: int = 0) -> Any:
        """
        Gets the first value from the dictionary.
        :param dict_: The dictionary to get first value of.
        :param index: The index of the value to get.
        :return: The first value from the dictionary.
        """
        key = DictUtil.get_key_by_index(dict_, index)
        if key:
            return dict_[key]

    @staticmethod
    def group_by(objs: List[Dict], key_lambda: Callable[[Dict], str]) -> Dict[str, List[Dict]]:
        """
        Groups list of objects using lambda to get key for object.
        :param objs: The objects to group.
        :param key_lambda: The lambda defining key for each object.
        :return: map of group to objects.
        """
        grouped_items = {}
        for obj in objs:
            obj_key = key_lambda(obj)
            DictUtil.set_or_append_item(grouped_items, obj_key, obj)
        return grouped_items
