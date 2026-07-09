import logging
import sys
import os
from logging.handlers import RotatingFileHandler

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

def setup_logger(name: str = "lexiforge"):
    logger = logging.getLogger(name)
    
    # Avoid attaching handlers multiple times
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # File Handler with Rotation (10MB max per file, keep 5 backups)
    file_handler = RotatingFileHandler(
        "logs/app.log", maxBytes=10*1024*1024, backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logger()
