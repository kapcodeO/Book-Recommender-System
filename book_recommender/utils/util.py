import yaml
import sys
from book_recommender.logging.log import logger
from book_recommender.exception.exception_handler import AppException

def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns the contents as a dictionary
    file_path: str
    """
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        logger.error(e)
        raise AppException(e, sys) from e