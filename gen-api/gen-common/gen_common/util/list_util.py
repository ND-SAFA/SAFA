from typing import Any, Iterable, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from scipy.stats import percentileofscore
from tqdm import tqdm


class ListUtil:
    """
    Provides list utility methods.
    """

    @staticmethod
    def flatten(list_: List[List]) -> List:
        """
        Flattens list of lists into single list.
        :param list_: List containing lists as elements.
        :return: List containing all sub-elements.
        """
        return [item for sublist in list_ for item in sublist]

    @staticmethod
    def get_n_items_from_list(list_: List, n_items: int, iteration_num: int = None, init_index: int = None) -> Tuple[List, int]:
        """
        Returns the start and end index to get n items from a list starting from a initial index
        :param list_: the list to retrieve items from
        :param n_items: the number of items to get from list
        :param iteration_num: if provided, will determine what items were used in prior iterations to calculate the start index
        :param init_index: if provided, will be the start index
        :return: a list of n_items from the list and the index to start from next if iterating
        """
        if iteration_num is None and init_index is None:
            raise Exception("Must provide a iteration number of the initial index")
        start = n_items * iteration_num if init_index is None else init_index
        end = start + n_items
        return list_[start:end], end

    @staticmethod
    def batch(iterable: List, n: int = 1):
        """
        Creates batches of constant size except for possible the last batch.
        :param iterable: The iterable containing items to batch.
        :param n: The batch size.
        :return: List of batches
        """
        iterable_len = len(iterable)
        batches = []
        for ndx in range(0, iterable_len, n):
            batches.append(iterable[ndx:min(ndx + n, iterable_len)])
        return batches

    @staticmethod
    def assert_equal(arrays) -> None:
        """
        Asserts that arrays contain the same elements.
        :param arrays: The arrays to verify.
        :return: None
        """
        arr_sizes = [len(l) for l in arrays]
        ListUtil.assert_mono_array(arr_sizes)

        labels_arr = np.array(arrays)
        np.apply_along_axis(func1d=ListUtil.assert_mono_array, arr=labels_arr, axis=0)

    @staticmethod
    def assert_mono_array(arr, default_msg: str = None) -> None:
        """
        Asserts that array has same values.
        :param arr: The array to assert.
        :param default_msg: The message to display on failure.
        :return: None
        """
        msg = f"Expected all label sizes to be equal: {arr}" if default_msg is None else default_msg
        assert len(set(arr)) == 1, msg

    @staticmethod
    def create_step_list(n: int, max_score=1.0, min_score=0.0, ascending=False):
        """
        Creates a list with scores decreasing linearly from max to min score.
        :param n: The length of the list.
        :param max_score: The score of the first item.
        :param min_score: The score of the last item.
        :param ascending: If numbers should be ascending in order.
        :return: The list of scores.
        """
        if n == 1:
            return [max_score]
        increment = (max_score - min_score) / (n - 1)  # Calculate the increment between numbers
        descending_list = [max_score - i * increment for i in range(n)]  # Generate the descending list
        if ascending:
            descending_list = sorted(descending_list)
        return descending_list

    @staticmethod
    def get_percentiles(scores: List[float]) -> List[float]:
        """
        Converts scores to percentiles.
        :param scores: The scores to convert.
        :return: List of percentiles.
        """
        scores_sorted = sorted(scores)
        s = pd.Series(scores)
        percentiles = s.apply(lambda x: percentileofscore(scores_sorted, x)) / 100
        return list(percentiles)

    @staticmethod
    def convert_numpy_array_to_native_types(numpy_array: np.ndarray) -> List:
        """
        Converts all items in a numpy array into native python objects
        :param numpy_array: The numpy array to convert
        :return:
        """
        return [i.item() for i in numpy_array]

    @staticmethod
    def selective_tqdm(iterable: Iterable, length_threshold: int = 3, **tqdm_args) -> Iterable:
        """
        Uses tqdm only if the iterable is greater than a given threshold.
        :param iterable: The object being iterated through.
        :param length_threshold: If the length of the iterable exceeds the threshold, tqdm is used.
        :param tqdm_args: Additional args to tqdm.
        :return: An iterable, either using tqdm if its long or just the original iterable if short.
        """
        return tqdm(iterable, **tqdm_args) if len(iterable) >= length_threshold else iterable

    @staticmethod
    def zip_sort(list1: List, list2: List, list_to_sort_on: int = 1, return_both: bool = True, **kwargs) -> List:
        """
        Sorts the items in two lists by the value in list_to_sort_on.
        :param list1: The first list.
        :param list2: The second list.
        :param list_to_sort_on: 0 if sort on the first list, 1 if sort on second.
        :param return_both: If True, returns both lists as a list of tuples, else only returns the list that was not used to sort.
        :param kwargs: Additional arguments to sorted.
        :return: Returns both lists as a list of tuples if return_both, else only returns the list that was not used to sort.
        """
        sorted_list = sorted(zip(list1, list2), key=lambda item: item[list_to_sort_on], **kwargs)
        list_to_return = 1 - list_to_sort_on
        return [item if return_both else item[list_to_return] for item in sorted_list]

    @staticmethod
    def unzip(zipped_list: List, item_index: int = None) -> Union[List, Tuple[List, List]]:
        """
        Returns list containing items at index in zipped list.
        :param zipped_list: List of zipped items.
        :param item_index: The index of the items to extract. If not provided, both lists are returned
        :return: List of items at index, or both lists unziped.
        """
        if item_index is not None:
            return [i[item_index] for i in zipped_list]
        else:
            return ListUtil.unzip(zipped_list, 0), ListUtil.unzip(zipped_list, 1)

    @staticmethod
    def zip_sort_unzip(*args, list_to_sort_on: int = None, **kwargs):
        """
        Sorts lists by zipping them then unzipping them.
        :param args: Lists to sort.
        :param list_to_sort_on: Index of list to sort on.
        :param kwargs: Additional arguments to zip_sort.
        :return: Unzip lists in sorted order.
        """
        if list_to_sort_on is None:
            list_to_sort_on = len(args)
        return ListUtil.unzip(ListUtil.zip_sort(*args, list_to_sort_on=list_to_sort_on, **kwargs))

    @staticmethod
    def safely_get_item(item_index: int, list_: List, default: Any = None) -> Any:
        """
        Safely gets an item from a list by checking that the list contains an item at the index, returns the default if not.
        :param item_index: The index of the item to get.
        :param list_: The list to get the item from.
        :param default: Default value to return if index does not exist.
        :return: The item from a list if it exists, returns the default if not.
        """
        required_length = item_index + 1 if item_index >= 0 else abs(item_index)
        return list_[item_index] if len(list_) >= required_length else default

    @staticmethod
    def are_all_items_the_same(list_: List) -> bool:
        """
        Checks if all items in the list are the same.
        :param list_: The list to check.
        :return: True if all items in the list are the same else False.
        """
        try:
            return len(set(list_)) == 1
        except TypeError:  # not hashable
            return all([item1 == item2 for item1 in list_ for item2 in list_])

    @staticmethod
    def get_max_value_with_index(list_: List) -> Tuple[int, Any]:
        """
        Gets the index of the max value in the list.
        :param list_: The list to get max of.
        :return: The index of the max value in the list.
        """
        return max(enumerate(list_), key=lambda item: item[1])

    @staticmethod
    def append_if_exists(base_items: List[Any], new_possible_item: Optional[Any], as_new_list: bool = False) -> List[Any]:
        """
        Appends new item to list if it exists.
        :param base_items: The base list to append to.
        :param new_possible_item: The possible item to add to list.
        :param as_new_list: Whether to create a new list, leaving the original list unaffected.
        :return: List of items which new item appended if it existed.
        """
        if as_new_list:
            base_items = [b for b in base_items]
        if new_possible_item:
            base_items.append(new_possible_item)
        return base_items

    @staticmethod
    def number_items(items: List[str], starting_num: int = 1) -> List[str]:
        """
        Adds number to each item in the list.
        :param items: List of strings to number
        :param starting_num: The number to start the list with.
        :return: A list of strings with their associated number.
        """
        return [f"{i+starting_num}: {item}" for i, item in enumerate(items)]
