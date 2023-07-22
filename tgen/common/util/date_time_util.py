from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class DateTimeUtil:
    """
    Provide utility methods for dealing with datetime objects.
    """

    @staticmethod
    def read_datetime(datetime_str: str, format: str = DATETIME_FORMAT):
        """
        Reads datetime string.
        :param datetime_str: The string defining date time.
        :param format: The format the string is in.
        :return: DateTime object.
        """
        return None if datetime_str == "None" or datetime_str is None else datetime.strptime(datetime_str, format)
