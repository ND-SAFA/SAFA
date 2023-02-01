from logging import Logger

from train.trainer_tools.trace_accelerator import TraceAccelerator
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
        if TraceAccelerator.is_main_process:
            super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel)

    def log_with_title(self, title: str, message: str) -> None:
        """
        Logs the message with a title
        :param title: The title to the message
        :param message: The message
        :return: None
        """
        title_border = '-' * max(round(len(message) / 2), 10)
        title = f"{title_border} {title} {title_border}"
        msg = f"{title}\n{message}"
        self.info(msg)
