"""
logger.py

This module provides a Logger class for tracking events, errors, and debug messages.
It uses Python's built-in logging module to log messages with various severity levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
The Logger class is designed to be modular and scalable, so that it can be easily integrated into larger systems and extended in the future.

Usage:
    from logger import Logger

    # Initialize logger
    logger = Logger(log_file="app.log", level="DEBUG")

    # Log messages
    logger.debug("This is a debug message")
    logger.info("Application started")
    logger.warning("This is a warning message")
    logger.error("An error occurred", exc_info=True)
    logger.critical("Critical error! System shutting down")
"""

import logging
import os
from logging import Logger as BaseLogger
from typing import Optional

class Logger:
    """
    A wrapper around Python's logging module to provide a simple and scalable logging interface.
    """

    def __init__(self, log_file: Optional[str] = None, level: str = "INFO") -> None:
        """
        Initializes the logger.

        :param log_file: Path to the log file. If None, logs will be output to console only.
        :param level: Logging level as string ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL").
        """
        self.logger: BaseLogger = logging.getLogger("SnakeGameLogger")
        self.logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        self.logger.propagate = False  # Prevent duplicate log entries if root logger is configured elsewhere

        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Clear existing handlers (if any)
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File handler, if log_file is provided
        if log_file:
            # Ensure directory exists
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
            file_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message: str, *args, **kwargs) -> None:
        """Logs a debug message."""
        self.logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs) -> None:
        """Logs an informational message."""
        self.logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs) -> None:
        """Logs a warning message."""
        self.logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs) -> None:
        """Logs an error message."""
        self.logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs) -> None:
        """Logs a critical error message."""
        self.logger.critical(message, *args, **kwargs)

