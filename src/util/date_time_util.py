from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class DateTimeUtil:
    """
    Provide utility methods for dealing with datetime objects.
    """

    @staticmethod
    def read_datetime(query: str):
        """

        :param query:
        :return:
        """
        return None if query == "None" or query is None else datetime.strptime(query, DATETIME_FORMAT)
