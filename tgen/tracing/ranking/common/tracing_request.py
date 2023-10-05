from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class TracingRequest:
    """
    Contains the information to tracing a single level.
    """
    child_ids: List[str]
    parent_ids: List[str]
    artifact_map: Dict[str, str]

    def get_tracing_pairs(self) -> List[Tuple[str, str]]:
        """
        Gets each parent, child pair
        :return: A list of parent, child pairs
        """
        pairs = []
        for parent_id in self.parent_ids:
            for child_id in self.child_ids:
                pairs.append((child_id, parent_id))
        return pairs

    def get_children_content(self) -> List[str]:
        """
        Gets the content for all children ids
        :return: A list of content for each child id
        """
        return self._get_artifact_content(self.child_ids)

    def get_parent_content(self) -> List[str]:
        """
          Gets the content for all parent ids
          :return: A list of content for each parent id
          """
        return self._get_artifact_content(self.parent_ids)

    def _get_artifact_content(self, artifact_ids: List[str]):
        """

        :param artifact_ids:
        :return:
        """
        contents = []
        for art_id in artifact_ids:
            contents.append(self.artifact_map[art_id])
        return contents
