from enum import Enum


class ChangeType(Enum):
    ADDED = "added"
    DELETED = "deleted"
    MODIFIED = "modified"
    RENAMED = "renamed"

    DEPENDENCIES = "dependencies"
    RENAMED_VARS = "renamed vars"
    NEW_FUNC = "new functionality"
    MODIFIED_FUNC = "modified functionality"
    BUG_FIXES = "bug fixes"
    REFACTORED = "refactored"
