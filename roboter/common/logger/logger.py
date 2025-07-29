import logging
from logging.config import fileConfig
from typing import Optional

# Some exporting manipulations to make unified access
# to logging

GREY = "\x1b[38;20m"
YELLOW = "\x1b[33;20m"
RED = "\x1b[31;20m"
ULTRA_RED = "\x1b[31;1m"
RESET = "\x1b[0m"


class __LoggerManager:
    def __init__(
        self,
    ):
        self.logger: Optional[logging.Logger] = None

    def get_logger(self):
        if self.logger is None:
            self.logger = logging.getLogger("unconfigured")
        return self.logger

    def configure_logger(self, config_file: str, name: str):
        fileConfig(config_file, disable_existing_loggers=True)
        self.logger = logging.getLogger(name)


__logger_manager = __LoggerManager()


def get_logger():
    return __logger_manager.get_logger()


def configure_logger(config_file: str, name: str):
    __logger_manager.configure_logger(config_file, name)


def info(msg: str):
    __logger_manager.get_logger().info(GREY + msg + RESET)


def debug(msg: str):
    __logger_manager.get_logger().debug(GREY + msg + RESET)


def warning(msg: str):
    __logger_manager.get_logger().warning(YELLOW + msg + RESET)


def error(msg: str):
    __logger_manager.get_logger().error(RED + msg + RESET)


def fatal(msg: str):
    __logger_manager.get_logger().fatal(ULTRA_RED + msg + RESET)
