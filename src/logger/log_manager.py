"""
    This module manages the async logger for the app.
    It uses the python logging module configured with files.
    A customized handler makes it compatible with async.
"""
# IMPORTS
from queue import SimpleQueue as Queue
from typing import List
import asyncio
import json
import logging
import logging.config


# CONSTANT DEFINITIONS
LOG_CONFIG_FILE_DEFAULT = "config/logger_config.json"


# CLASSES
class LocalQueueHandler(logging.handlers.QueueHandler):
    """
        Custom QueueHandler used as the proxy handler
        of the async logging system.
    """
    def emit(self, record: logging.LogRecord) -> None:
        """Removed the call to self.prepare(), handle task cancellation"""
        # pylint: disable=broad-exception-caught
        try:
            self.enqueue(record)
        # pylint: disable=try-except-raise
        except asyncio.CancelledError:
            raise
        # pylint: enable=try-except-raise
        except Exception:
            self.handleError(record)
        # pylint: enable=broad-exception-caught


# METHODS
def _setup_logging_queue(logger_name: str = '') -> None:
    """Move log handlers to a separate thread.

    Replace handlers on the root logger with a LocalQueueHandler,
    and start a logging.QueueListener holding the original
    handlers.

    Input:
        - logger_name: name of the logger to setup as async
            By default, the top-level logger of the app.

    """

    # Create the queue handler
    logging_queue = Queue()
    queue_handler = LocalQueueHandler(logging_queue)

    original_handlers: List[logging.Handler] = []

    root_logger = logging.getLogger(logger_name)
    root_logger.addHandler(queue_handler)

    # Displace all existing handlers after the queue
    for handler in root_logger.handlers[:]:
        if handler is not queue_handler:
            root_logger.removeHandler(handler)
            original_handlers.append(handler)

    listener = logging.handlers.QueueListener(
        logging_queue, *original_handlers, respect_handler_level=True
    )
    listener.start()


def setup_logger(is_async: bool = True, logger_name: str = '',
                 logger_config_path: str = LOG_CONFIG_FILE_DEFAULT):
    """
        Configure the logging system from a file and set up one logger to be async.

        Inputs:
            - logger_name: Name of the logger
            - logger_config_path: Path to the config json file to apply to the logger.
    """

    # Local status variables
    is_logger_config_valid = False  # Did we manage to load and apply the config file ?
    io_error = None  # Buffer for the IOError message
    config_error = None  # buffer for dictConfig error messages

    # Load config file and apply
    try:
        with open(logger_config_path, encoding='utf-8') as logger_config_file:
            logger_config = json.load(logger_config_file)
            logging.config.dictConfig(logger_config)
            is_logger_config_valid = True
    # Errors must be buffered, waiting for the logger to be ready, so that they can be logged.
    except IOError as error:
        io_error = error
    except (ValueError, TypeError, AttributeError, ImportError) as error:
        config_error = error

    # Turn the logger into an async logger
    if is_async is True:
        _setup_logging_queue(logger_name)

    # Log results
    logger = logging.getLogger(__name__)
    if is_logger_config_valid is True:
        logger.info('Async logger successfully configured.')
    else:
        logger.info('Async logger started without specific configuration.')
        if io_error is not None:
            logger.warning(
                'setup_logger - IOError while retrieving the logger configuration file:%s',
                io_error)
        if config_error is not None:
            logger.warning(
                'setup_logger - Error while configuring the logger:%s', config_error)
