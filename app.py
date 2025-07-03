import sys
from book_recommender.logging.log import logger  # Import the logger from log.py
from book_recommender.exception.exception_handler import AppException
try:
    print(3/0)
except Exception as e:
    logger.error(e)
    raise AppException(e, sys) from e