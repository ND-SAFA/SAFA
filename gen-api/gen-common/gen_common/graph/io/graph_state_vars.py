from typing import Type

from gen_common.graph.io.graph_state import GraphState
from gen_common.graph.io.state_to_prompt_converters import ContextPromptConverter, DocumentPromptConverter
from gen_common.graph.io.state_var import StateVar
from gen_common.graph.io.state_var_prompt_config import StateVarPromptConfig


class GraphStateVars:
    USER_QUESTION = StateVar("user_question")
    ART_REF_IN_QUESTION = StateVar("artifacts_referenced_in_question",
                                   prompt_config=StateVarPromptConfig(prompt_converter=ContextPromptConverter))
    CHAT_HISTORY = StateVar("chat_history", prompt_config=StateVarPromptConfig(include_in_message_prompt=False))
    GENERATION = StateVar("generation")
    REFERENCE_IDS = StateVar("reference_ids")
    DOCUMENTS = StateVar("documents", prompt_config=StateVarPromptConfig(prompt_converter=DocumentPromptConverter))
    RETRIEVAL_QUERY = StateVar("retrieval_query")
    ARTIFACT_TYPES = StateVar("artifact_types")
    SELECTED_ARTIFACT_IDS = StateVar("selected_artifact_ids")
    TOOLS_ALREADY_USED = StateVar("tools_already_used")
    RELEVANT_INFORMATION = StateVar("relevant_information_learned")
    RELATED_DOC_IDS = StateVar("related_doc_ids")
    RUN_ASYNC = StateVar("run_async")
    THREAD_ID = StateVar("thread_id")
    BLACKLISTED_TOOLS = StateVar("backlisted_tools")

    @classmethod
    def validate(cls, state_cls: Type[GraphState] = GraphState) -> None:
        """
        Validates that all variables exist in the state.
        :param state_cls: The state class.
        :return: None
        """
        for value in vars(cls).values():
            if isinstance(value, StateVar):
                assert value.var_name in state_cls.__annotations__, f"Unknown state value {value.var_name}"


GraphStateVars.validate()
