from typing import Dict, List, Set, Tuple, TypedDict

from langchain_core.documents.base import Document

from gen_common.util.enum_util import EnumDict


class GraphState(TypedDict, total=False):
    """
    Represents the state of our chat.
    """
    # args
    user_question: str
    context_filepath: str  # only used for testing purposes
    chat_history: List[Tuple[str, str]]
    artifacts_referenced_in_question: List[EnumDict]

    # generation
    generation: str
    reference_ids: List[str]

    # context retrieval
    documents: Dict[str, List[Document]]
    retrieval_query: str | Set[str]
    artifact_types: List[str]
    selected_artifact_ids: Set[str]

    # request assistance
    relevant_information_learned: str
    related_doc_ids: List[str]

    # tools
    tools_already_used: List[str]

    # settings
    run_async: bool
    thread_id: str


def has_state_value(state: GraphState, var_name: str) -> bool:
    """
    Checks if the value is defined in the current state.
    :param state: The state.
    :param var_name: The name of the variable to check for.
    :return: True if the value is defined in the current state else False.
    """
    if var_name not in state:
        return False
    val = state.get(var_name)
    if val is None:
        return False
    elif hasattr(val, "__len__") and len(val) == 0:
        return False

    return True
