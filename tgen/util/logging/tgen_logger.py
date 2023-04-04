from logging import Logger

from util.override import overrides


class TGenLogger(Logger):
    """
    Handles Logging for TGEN
    """

    @overrides(Logger)
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1) -> None:
        """
        Ensures that logging only occurs on main process (see Python logging docs for details on params)
        :return: None
        """
        super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel)

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
