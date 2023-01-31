from dataclasses import dataclass

from config.constants import LOG_LEVEL_DEFAULT, LOG_FILE_DEFAULT, VERBOSE_DEFAULT, LOG_TO_CONSOLE_DEFAULT


@dataclass
class LoggerConfig:
    log_level: int = LOG_LEVEL_DEFAULT
    log_filename: str = LOG_FILE_DEFAULT
    verbose: bool = VERBOSE_DEFAULT
    log_to_console: bool = LOG_TO_CONSOLE_DEFAULT
    output_dir: str = None
