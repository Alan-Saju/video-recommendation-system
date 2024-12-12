# utils/logging_config.py
import logging
import os
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_logging():
    """
    Configure logging for the application
    """
    # Ensure log directory exists
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)

    # Configure logging
    log_file = os.path.join(log_dir, os.getenv('LOG_FILE', 'recommendation_system.log'))
    log_level = getattr(logging, os.getenv('LOG_LEVEL', 'INFO').upper())

    # Create a custom logger
    logger = logging.getLogger('recommendation_system')
    logger.setLevel(log_level)

    # Create handlers
    c_handler = logging.StreamHandler()  # Console handler
    f_handler = RotatingFileHandler(
        log_file, 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    
    # Create formatters and add it to handlers
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    c_handler.setFormatter(log_format)
    f_handler.setFormatter(log_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger

# Global logger instance
logger = setup_logging()