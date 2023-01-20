from typing import List, Tuple


class ListUtil:
    """
    Provides list utility methods.
    """

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
