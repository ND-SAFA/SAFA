from logging import Logger


class TGenLogger(Logger):
    """
    Handles Logging for TGEN
    """
    DEFAULT_LOG_LENGTH = 100

    def log_with_title(self, title: str, message: str) -> None:
        """
        Logs the message with a title
        :param title: The title to the message
        :param message: The message
        :return: None
        """
        message = "" if message is None else message
        title = TGenLogger.__create_title(title, message)
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
    def __create_title(title: str, message: str = ""):
        message = "" if message is None else message
        title_border = '-' * min(max(round(len(title) / 2), 10), TGenLogger.DEFAULT_LOG_LENGTH)
        title = f"{title_border} {title} {title_border}"
        return title
