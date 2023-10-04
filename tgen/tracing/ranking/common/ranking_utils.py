from dataclasses import dataclass
from typing import Dict, List, Tuple

from tgen.common.util.enum_util import EnumDict
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.trace_dataframe import TraceKeys


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


def extract_tracing_requests(artifact_df: ArtifactDataFrame, layers: List[Tuple[str, str]]) -> List[TracingRequest]:
    """
    Extracts source and target artifact names for each layer
    :param artifact_df: Artifact data frame containing ids, bodies, and types.
    :param layers: The layers being traced, containing list of (child, parent) tuples.
    :return:
    """
    requests = []
    artifact_map = artifact_df.to_map()
    for child_type, parent_type in layers:
        parent_df = artifact_df.get_type(parent_type)
        child_df = artifact_df.get_type(child_type)

        parent_names = list(parent_df.index)
        child_names = list(child_df.index)
        requests.append(TracingRequest(child_ids=child_names, parent_ids=parent_names, artifact_map=artifact_map))
    return requests


def create_entry(parent: str, child: str, score: float = 0.0) -> EnumDict:
    """
    Creates a prediction entry
    :param parent: The parent artifact id
    :param child: The child artifact id
    :param score: The score representing strength of link between child + parent
    :return: a prediction entry
    """
    return EnumDict({
        TraceKeys.TARGET: parent,
        TraceKeys.SOURCE: child,
        TraceKeys.SCORE: score
    })


def convert_parent2rankings_to_prediction_entries(parent2rankings: Dict[str, List]) -> Dict[str, List[EnumDict]]:
    """
    Converts the parent2ranking dictionary produced by the sorters into a list of prediction entries
    :param parent2rankings: The dictionary produced by the sorter containing parent art id mapped to ordered children
    :return: A list of enum dictionaries representing a prediction entry for each parent, child pair
    """
    prediction_entries = {}
    for parent, parent_payload in parent2rankings.items():
        prediction_entries[parent] = []
        for child, score in zip(*parent_payload):
            entry = create_entry(parent, child, score)
            prediction_entries[parent].append(entry)
    return prediction_entries
