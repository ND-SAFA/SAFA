from dataclasses import dataclass
from typing import Dict, List, Tuple

from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame


@dataclass
class TracingRequestIds:
    """
    Contains ids to trace between.
    """
    child_ids: List[str]
    parent_ids: List[str]


@dataclass
class TracingRequest(TracingRequestIds):
    """
    Contains the information to tracing a single level.
    """
    artifact_map: Dict[str, str]

    def get_tracing_pairs(self) -> List[Tuple[str, str]]:
        pairs = []
        for parent_id in self.parent_ids:
            for child_id in self.child_ids:
                pairs.append((child_id, parent_id))
        return pairs

    def get_children_content(self) -> List[str]:
        return self._get_artifact_content(self.child_ids)

    def get_parent_content(self):
        return self._get_artifact_content(self.parent_ids)

    def _get_artifact_content(self, artifact_ids: List[str]):
        children = []
        for child_id in artifact_ids:
            children.append(self.artifact_map[child_id])
        return children


def extract_tracing_requests(artifact_df: ArtifactDataFrame, layers: List[Tuple[str, str]]) -> List[TracingRequest]:
    """
    Extracts source and target artifact names for each layer
    :param artifact_df: Artifact data frame containing ids, bodies, and types.
    :param layers: The layers being traced, containing list of (child, parent) tuples.
    :return:
    """
    requests = []
    artifact_map = artifact_df.get_map()
    for child_type, parent_type in layers:
        parent_df = artifact_df.get_type(parent_type)
        child_df = artifact_df.get_type(child_type)

        parent_names = list(parent_df.index)
        child_names = list(child_df.index)
        requests.append(TracingRequest(child_ids=child_names, parent_ids=parent_names, artifact_map=artifact_map))
    return requests
