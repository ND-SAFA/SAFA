from abc import abstractmethod

from typing import List, Dict

from gen_common.util.enum_util import EnumDict


class iFilter:

    @staticmethod
    @abstractmethod
    def filter(parent2children: Dict[str, List[EnumDict]], children_ids: List[str], parent_ids: List[str],
               **kwargs) -> Dict[str, List]:
        """
        Filters the children artifacts and sets filtered out children scores to 0.
        :param parent2children: Maps parent id to a list of its children ids and a list of their associated scores.
        :param children_ids: List of ids of each child artifact.
        :param parent_ids: List of ids of each parent artifact.
        :return: Map of parent to list of sorted children traces with non-selected children scores set to 0.
        """
