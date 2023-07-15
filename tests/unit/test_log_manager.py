"""
This file contains unit tests for log_manager.py
"""
# --- IMPORTS ---
import logging
import pytest
from src.logger.log_manager import setup_logger
# ---


@pytest.mark.parametrize("logger_config_path", [
    (None),
    ('a_wrong_path'),
])
def test_setup_logger_default_completion(logger_config_path):
    """
        Checks that setup_logger runs successfully with various configurations.
    """
    success = False
    logging.basicConfig(force=True)
    try:
        if logger_config_path is None:
            setup_logger(True)
        else:
            setup_logger(True, logger_config_path)
        success = True
    finally:
        assert success is True
