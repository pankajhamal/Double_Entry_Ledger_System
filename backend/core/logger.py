import logging 
import sys
from logging.handlers import RotatingFileHandler

def setup_logger():
    logger = logging.getLogger("fast_api")

    logger.setLevel(logging.INFO)

    #avoid duplicate handler
    if logger.handlers:
        return logger

    #Console handler
    console_handler = logging.StreamHandler(sys.stdout)

    console_handler.setLevel(logging.INFO)

     # File handler
    file_handler = RotatingFileHandler(
        "app.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5
    )

    file_handler.setLevel(logging.ERROR)

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)


    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


    return logger


logger = setup_logger()