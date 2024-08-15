from enum import Enum
from types import DynamicClassAttribute

from common_resources.llm.prompts.prompt import Prompt

from tgen.prompts.supported_prompts.supported_prompts import SupportedPrompts


class ArtifactSummaryTypes(Enum):
    CODE_BASE = SupportedPrompts.CODE_SUMMARY
    NL_BASE = SupportedPrompts.NL_SUMMARY

    @DynamicClassAttribute
    def value(self) -> Prompt:
        """Overrides getting the value of the Enum member to return a copy."""
        return self._value_.value
