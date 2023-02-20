from util.supported_enum import SupportedEnum


class GithubArtifactType(SupportedEnum):
    """
    The different types of GitHub artifacts scraped.
    """
    ISSUE = "issue"
    COMMIT = "commit"
    LINK = "link"
    PULL_REQUEST = "pull_request"
