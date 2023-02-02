import logging
import os
import sys
from os.path import dirname
from typing import Any, Optional

from huggingface_hub.utils import logging as hf_logging

from constants import LOG_FORMAT
from util.file_util import FileUtil
from util.logging.logger_config import LoggerConfig
from util.logging.tgen_logger import TGenLogger


class LoggerManager:
    __logger: Optional[TGenLogger] = None
    __logger_is_configured = False

    @staticmethod
    def configure_logger(logger_config: LoggerConfig) -> TGenLogger:
        """
        Setups the logger to use for TGEN
        :param logger_config: Configurations for the logger
        :return: the Logger
        """
        if LoggerManager.__logger_is_configured:
            curr_logger = LoggerManager.get_logger()
            curr_logger.warning("Logger is already configured. Using existing logger.")
            return curr_logger
        LoggerManager.__logger_is_configured = True
        LoggerManager.__logger: TGenLogger = logging.getLogger("tgen")
        logger.setLevel(logger_config.log_level)
        log_filepath = os.path.join(logger_config.output_dir, logger_config.log_filename) \
            if logger_config.output_dir else logger_config.log_filename
        FileUtil.create_dir_safely(dirname(log_filepath))
        file_handler = logging.FileHandler(log_filepath)
        console_handler = logging.StreamHandler(sys.stdout)

        default_formatter = logging.Formatter(LOG_FORMAT, datefmt='%m/%d %H:%M:%S')
        formatters = [default_formatter]
        if logger_config.verbose:
            formatters.append(default_formatter)
        else:
            formatters.append(logging.Formatter("%(message)s"))

        for i, handler in enumerate([file_handler, console_handler]):
            handler.setLevel(logger_config.log_level)
            handler.setFormatter(formatters[i])

        if logger_config.log_to_console:
            LoggerManager.__logger.addHandler(console_handler)
        LoggerManager.__logger.addHandler(file_handler)

        return LoggerManager.__logger

    @staticmethod
    def get_logger() -> TGenLogger:
        """
        Gets the logger for TGen
        :return: The Logger
        """
        if LoggerManager.__logger is None:
            LoggerManager.__logger = LoggerManager.configure_logger(LoggerConfig())
        return LoggerManager.__logger

    @staticmethod
    def turn_off_hugging_face_logging() -> None:
        """
        Turns off all logging for hugging face
        :return: None
        """
        for module in sys.modules.keys():
            if module.startswith("transformers"):
                hf_logger = hf_logging.get_logger(module)
                hf_logger.setLevel(logging.ERROR)

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


logging.setLoggerClass(TGenLogger)
LoggerManager.turn_off_hugging_face_logging()
logger: TGenLogger = LoggerManager()
