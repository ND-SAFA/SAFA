import logging
import os
from logging import Logger
from typing import Optional

from config.constants import LOG_FORMAT
from config.override import overrides
from train.trace_accelerator import TraceAccelerator
from util.logging.logger_config import LoggerConfig


class TgenLogger(Logger):
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


logging.setLoggerClass(TgenLogger)
__logger: Optional[TgenLogger] = None


def setup_logger(logger_config: LoggerConfig) -> TgenLogger:
    """
    Setups the logger to use for TGEN
    :param logger_config: Configurations for the logger
    :return: the Logger
    """
    global __logger
    __logger: TgenLogger = logging.getLogger("root")
    log_filepath = os.path.join(logger_config.output_dir, logger_config.log_filename) \
        if logger_config.output_dir else logger_config.log_filename
    file_handler = logging.FileHandler(log_filepath)
    console_handler = logging.StreamHandler()

    default_formatter = logging.Formatter(LOG_FORMAT, datefmt='%d/%m/%Y %H:%M:%S')
    formatters = [default_formatter]
    if logger_config.verbose:
        formatters.append(default_formatter)
    else:
        formatters.append(logging.Formatter("%(message)s"))

    for i, handler in [file_handler, console_handler]:
        handler.setLevel(logger_config.log_level)
        handler.setFormatter(formatters[i])

    if logger_config.log_to_console:
        __logger.addHandler(console_handler)
    __logger.addHandler(file_handler)
    return __logger


def get_logger() -> TgenLogger:
    """
    Gets the logger for TGen
    :return: The Logger
    """
    global __logger
    if __logger is None:
        __logger = setup_logger(LoggerConfig())
    return __logger
