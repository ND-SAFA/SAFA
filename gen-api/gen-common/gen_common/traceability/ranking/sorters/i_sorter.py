from abc import abstractmethod

from typing import List, Dict


class iSorter:

    @staticmethod
    @abstractmethod
    def sort(parent_ids: List[str], child_ids: List[str], artifact_map: Dict[str, str],
             return_scores: bool = False, **kwargs) -> Dict[str, List]:
        """
        Sorts the children artifacts from most to least similar to the parent artifacts.
        :param parent_ids: The artifact ids of the parents.
        :param child_ids: The artifact ids of the children.
        :param artifact_map: Map of ID to artifact bodies.
        :param return_scores: Whether to return the similarity scores
        :return: Map of parent to list of sorted children.
        """
