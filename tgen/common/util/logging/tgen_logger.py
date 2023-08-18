from logging import Logger

from tgen.constants.deliminator_constants import EMPTY_STRING


class TGenLogger(Logger):
    """
    Handles Logging for TGEN
    """
    DEFAULT_TITLE_LENGTH = 100

    def log_with_title(self, title: str, message: str = EMPTY_STRING) -> None:
        """
        Logs the message with a title
        :param title: The title to the message
        :param message: The message
        :return: None
        """
        message = "" if message is None else message
        title = TGenLogger.__create_title(title)
        msg = f"{title}\n{message}"
        self.info(msg)

    def log_title(self, title: str) -> None:
        """
        Logs the message with a title
        :param title: The title to the message
        :return: None
        """
        title_formatted = TGenLogger.__create_title(title)
        self.info(title_formatted)

    @staticmethod
    def __create_title(title: str):
        prefix_len = int((TGenLogger.DEFAULT_TITLE_LENGTH - len(title)) / 2)
        prefix_len = max(prefix_len, 0)
        title_border = '-' * prefix_len
        title = f"{title_border} {title} {title_border}".strip()
        return title
