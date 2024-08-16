import logging
import os
import sys
from os.path import dirname
from typing import Any, Optional

from gen_common.constants import LOG_FORMAT
from gen_common.infra.t_logging.logger_config import LoggerConfig
from gen_common.infra.t_logging.the_logger import TheLogger


class LoggerManager:
    __logger: Optional[TheLogger] = None
    __logger_is_configured = False

    @staticmethod
    def configure_logger(logger_config: LoggerConfig) -> TheLogger:
        """
        Setups the logger to use for TGEN
        :param logger_config: Configurations for the logger
        :return: the Logger
        """
        if LoggerManager.__logger_is_configured:
            curr_logger = LoggerManager.get_logger()
            return curr_logger
        LoggerManager.__logger_is_configured = True
        LoggerManager.__logger: TheLogger = logging.getLogger("the_logger")
        logger.setLevel(logger_config.log_level)

        console_handler = logging.StreamHandler(sys.stdout)
        handlers = [console_handler]
        file_handler = None
        if logger_config.output_dir:
            log_filepath = os.path.join(logger_config.output_dir, logger_config.log_filename)
            os.makedirs(dirname(log_filepath), exist_ok=True)
            file_handler = logging.FileHandler(log_filepath)
            handlers.append(file_handler)

        default_formatter = logging.Formatter(LOG_FORMAT, datefmt='%m/%d %H:%M:%S')
        formatters = [default_formatter] if logger_config.verbose else [logging.Formatter("%(message)s")]
        formatters.append(default_formatter)

        for i, handler in enumerate(handlers):
            handler.setLevel(logger_config.log_level)
            handler.setFormatter(formatters[i])

        if logger_config.log_to_console:
            LoggerManager.__logger.addHandler(console_handler)
        if file_handler is not None:
            LoggerManager.__logger.addHandler(file_handler)

        return LoggerManager.__logger

    @staticmethod
    def get_logger() -> TheLogger:
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
                from huggingface_hub.utils import logging as hf_logging
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


logging.setLoggerClass(TheLogger)
LoggerManager.turn_off_hugging_face_logging()
logger: TheLogger = LoggerManager()
logger.propagate = False
