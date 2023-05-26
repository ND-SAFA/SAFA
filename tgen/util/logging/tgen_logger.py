from logging import Logger


class TGenLogger(Logger):
    """
    Handles Logging for TGEN
    """

    def log_with_title(self, title: str, message: str) -> None:
        """
        Logs the message with a title
        :param title: The title to the message
        :param message: The message
        :return: None
        """
        message = "" if message is None else message
        title_border = '-' * min(max(round(len(message) / 2), 10), 50)
        title = f"{title_border} {title} {title_border}"
        msg = f"{title}\n{message}"
        self.info(msg)
