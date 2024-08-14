import random
from typing import List

from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.tools.constants.symbol_constants import UNDERSCORE


def expand_query_selection(artifact_df: ArtifactDataFrame, query_ids: List[str]) -> List[str]:
    """
    Expands query ids if a selection command is found.
    :param artifact_df: Artifact dataframe containing project artifacts.
    :param query_ids: List of query ids which may contain selection commands.
    :return: List of artifacts ids in query.
    """
    command = None
    if isinstance(query_ids, list) and len(query_ids) == 1:
        command = query_ids[0]
    elif isinstance(query_ids, str):
        command = query_ids

    if command:
        artifact_ids = list(artifact_df.index)
        command = command.upper()
        if command == ALL_SELECTION:
            query_ids = list(artifact_ids)
        if command == RANDOM_SELECTION:
            query_ids = [random.choice(artifact_ids)]

        if RANDOM_SELECTION in command:
            try:
                k = int(command.split(UNDERSCORE)[-1])
                query_ids = random.sample(artifact_ids, k)
            except Exception as e:
                pass

    return query_ids
