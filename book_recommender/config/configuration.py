import os
import sys
from book_recommender.logging.log import logger
from book_recommender.utils.util import read_yaml_file
from book_recommender.exception.exception_handler import AppException
from book_recommender.entity.config_entity import DataIngestionConfig
from book_recommender.constant import CONFIG_FILE_PATH

class AppConfiguration:
    def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
        try:
            self.configs_info = read_yaml_file(file_path=config_file_path)
        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            data_ingestion_config = self.configs_info["data_ingestion_config"]
            artifacts_dir = self.configs_info["artifacts_config"]["artifacts_dir"]
            dataset_dir = data_ingestion_config["dataset_dir"]

            ingested_data_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config["ingested_data_dir"])
            raw_data_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config["raw_data_dir"])

            response = DataIngestionConfig(
                dataset_download_url = data_ingestion_config["dataset_download_url"],
                ingested_dir = ingested_data_dir,
                raw_data_dir = raw_data_dir 
            )

            logger.info(f"Data Ingestion Config : {response}")
            return response
        
        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e