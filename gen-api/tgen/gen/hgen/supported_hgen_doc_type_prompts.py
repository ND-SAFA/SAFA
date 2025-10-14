from copy import deepcopy
from types import DynamicClassAttribute

from gen_common.llm.prompts.prompt import Prompt
from gen_common.constants.symbol_constants import UNDERSCORE
from gen_common.util.enum_util import EnumUtil
from gen_common.util.supported_enum import SupportedEnum

from gen.hgen.hgen_prompts import API_DATAFLOW_QUESTIONNAIRE, CLUSTERING_QUESTIONNAIRE, \
    DB_ENTITY_SPEC_QUESTIONNAIRE


class SupportedHGenDocPrompts(SupportedEnum):
    BASE = CLUSTERING_QUESTIONNAIRE
    API_DATAFLOW = API_DATAFLOW_QUESTIONNAIRE
    DB_ENTITY_SPEC = DB_ENTITY_SPEC_QUESTIONNAIRE

    @classmethod
    def get_prompt_by_type(cls, doc_type: str) -> "SupportedHGenDocPrompts":
        """
        Selects a prompt by the desired type.
        :param doc_type: The type of document being created.
        :return: A prompt to create the desired type.
        """
        e = EnumUtil.get_enum_from_name(cls, UNDERSCORE.join(doc_type.split()), raise_exception=False)
        return e if e is not None else SupportedHGenDocPrompts.BASE

    @DynamicClassAttribute
    def value(self) -> Prompt:
        """Overrides getting the value of the Enum member to return a copy."""
        return deepcopy(self._value_)
