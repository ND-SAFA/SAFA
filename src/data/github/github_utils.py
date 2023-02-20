from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class GithubUtils:
    """
    Contains utility methods for scraping github projects.
    """

    @staticmethod
    def read_datetime(query: str):
        return None if query == "None" or query is None else datetime.strptime(query, DATETIME_FORMAT)
