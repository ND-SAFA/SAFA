from gen_common.util.supported_enum import SupportedEnum


class GArtifactType(SupportedEnum):
    """
    The different types of GitHub artifacts scraped.
    """
    ISSUE = "issue"
    COMMIT = "commit"
    LINK = "link"
    PULL = "pull"
    CODE = "code"
