from enum import Enum
from typing import List

from itypes import List


class ChangeType(Enum):
    # HIGH-LEVEL  CATEGORIZATIONS (from GITHUB)
    ADDED = "added"
    DELETED = "deleted"
    MODIFIED = "modified"
    RENAMED = "renamed"

    # GRANULAR CATEGORIZATIONS
    DEPENDENCIES_IMPORTS = "dependencies"
    RENAMED_VARS = "renamed vars"
    NEW_FUNC = "new functionality"
    MODIFIED_FUNC = "modified functionality"
    BUG_FIXES = "bug fixes"
    REFACTORED = "refactored"
    REMOVED_FUNC = "removed functionality"

    @staticmethod
    def get_granular_change_type_categories() -> list["ChangeType"]:
        """
        Gets the change types that relate to more granular categorizations
        :return: List of change types that relate to more granular categorizations
        """
        return [ChangeType.MODIFIED_FUNC, ChangeType.NEW_FUNC, ChangeType.REMOVED_FUNC, ChangeType.BUG_FIXES,
                ChangeType.REFACTORED, ChangeType.DEPENDENCIES_IMPORTS, ChangeType.RENAMED_VARS]
