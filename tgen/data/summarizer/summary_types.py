from enum import Enum
from types import DynamicClassAttribute

from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.supported_prompts.supported_prompts import SupportedPrompts


class SummaryTypes(Enum):
    CODE_BASE = SupportedPrompts.CODE_SUMMARY
    NL_BASE = SupportedPrompts.NL_SUMMARY

    @DynamicClassAttribute
    def value(self) -> Prompt:
        """Overrides getting the value of the Enum member to return a copy."""
        return self._value_.value
