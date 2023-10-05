from typing import Dict, List, Tuple

from tgen.common.util.enum_util import EnumDict
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.tracing.ranking.common.tracing_request import TracingRequest


class RankingUtil:

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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
                entry = RankingUtil.create_entry(parent, child, score)
                prediction_entries[parent].append(entry)
        return prediction_entries
