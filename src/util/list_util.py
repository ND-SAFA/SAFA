from typing import List, Tuple

import numpy as np


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
