from types import DynamicClassAttribute

from extendableenum.extendableenum import inheritable_enum

from common_resources.tools.util.supported_enum import SupportedEnum

from common_resources.graph.branches.decide_after_generation_branch import DecideAfterGenerationBranch
from common_resources.graph.branches.grade_generation_branch import GradeGenerationBranch


@inheritable_enum
class SupportedBranches(SupportedEnum):
    GRADE_GENERATION = GradeGenerationBranch
    DECIDE_NEXT = DecideAfterGenerationBranch

    @DynamicClassAttribute
    def name(self) -> str:
        """Overrides getting the name of the Enum member to get version to use for langchain."""
        return self._name_.lower() if self._name_ != "END_COMMAND" else self._value_
