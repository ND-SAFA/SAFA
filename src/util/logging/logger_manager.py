import os
from typing import Optional, Any

from config.constants import LOG_FORMAT
from util.logging.logger_config import LoggerConfig
from util.logging.tgen_logger import TgenLogger
import logging

logging.setLoggerClass(TgenLogger)


class LoggerManager:
    __logger: Optional[TgenLogger] = None

    @staticmethod
    def setup_logger(logger_config: LoggerConfig) -> TgenLogger:
        """
        Setups the logger to use for TGEN
        :param logger_config: Configurations for the logger
        :return: the Logger
        """
        LoggerManager.__logger = logging.getLogger("root")
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
            LoggerManager.__logger.addHandler(console_handler)
        LoggerManager.__logger.addHandler(file_handler)
        return LoggerManager.__logger

    @staticmethod
    def get_logger() -> TgenLogger:
        """
        Gets the logger for TGen
        :return: The Logger
        """
        if LoggerManager.__logger is None:
            LoggerManager.__logger = LoggerManager.setup_logger(LoggerConfig())
        return LoggerManager.__logger

    @classmethod
    def __getattr__(cls, attr: str) -> Any:
        """
        Gets attribute from self if exists, otherwise will get from the logger
        :param attr: The attribute to get
        :return: The attribute value
        """
        if hasattr(cls, attr):
            return super().__getattribute__(cls, attr)
        return getattr(LoggerManager.get_logger(), attr)


logger = LoggerManager()
