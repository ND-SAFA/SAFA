from functools import lru_cache
from logging import Logger
from typing import Type

from tgen.common.constants.deliminator_constants import EMPTY_STRING


class TGenLogger(Logger):
    """
    Handles Logging for TGEN
    """
    DEFAULT_TITLE_LENGTH = 100

    def log_with_title(self, title: str, message: str = EMPTY_STRING, formatting: str = None) -> None:
        """
        Logs the message with a title
        :param title: The title to the message
        :param message: The message
        :param formatting: If provided, will use the string to format the title
        :return: None
        """
        message = EMPTY_STRING if message is None else message
        title = TGenLogger.__create_title(title) if not formatting else formatting.format(title)
        msg = f"{title}"
        if len(message) > 0:
            msg += f"\n{message}"
        self.info(msg)

    def log_title(self, title: str, **kwargs) -> None:
        """
        Logs the message with a title
        :param title: The title to the message
        :return: None
        """
        title_formatted = TGenLogger.__create_title(title, **kwargs)
        self.info(title_formatted)

    def log_step(self, step: str) -> None:
        """
        Logs the message as a new step.
        :param step: The name of the step.
        :return: None
        """
        step_formatted = TGenLogger.__create_step(step)
        self.info(step_formatted)

    @lru_cache(maxsize=5)
    def log_without_spam(self, level: int, msg: object, *args: object, **kwargs) -> None:
        """
        Logs a given message only once
        :param level: The level of the log (e.g. warning, error, info...)
        :param msg: The message to log
        :param args: Additional arguments to the log func
        :param kwargs: Additional parameters to the log func
        :return: None
        """
        return self.log(level=level, msg=msg, *args, **kwargs)

    def log_exception_on_condition(self, exception_class: Type[Exception], exception_msg: str, condition: bool = True) -> None:
        """
        Logs an exception and stack trace.
        :param exception_class: The class of the exception.
        :param exception_msg: The corresponding message of the exception.
        :param condition: Only logs if condition is True.
        :return: None.
        """
        try:
            raise exception_class(exception_msg)
        except Exception:
            if condition:
                self.exception(exception_msg)

    @staticmethod
    def __create_title(title: str, prefix: str = EMPTY_STRING):
        """
        Logs the message as a new title in the logs.
        :param title: The title name.
        :param prefix: Prefix to prepend title with.
        :return: Title formatted as markdown header.
        """
        title = prefix + f"# {title}".strip()
        return title

    @staticmethod
    def __create_step(step: str) -> str:
        """
        Logs the message as a new step in the logs.
        :param step: The name of the step.
        :return: Step formatted as markdown header.
        """
        formatted_step = f"## {step}"
        return formatted_step
