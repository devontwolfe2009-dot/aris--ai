"""
Logger Module
Handles logging configuration and setup
"""

import logging
import os
from datetime import datetime

def setup_logger(name):
    """
    Setup logger with console and file handlers
    
    Args:
        name (str): Logger name (usually __name__)
    
    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)
    
    # Only add handlers if they haven't been added yet
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        # Create logs directory if it doesn't exist
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # File handler
        log_file = os.path.join(log_dir, f'aris_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

# Create a root logger for ARIS
aris_logger = setup_logger('ARIS')
