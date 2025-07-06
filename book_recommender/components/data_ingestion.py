# STAGE 1

import os
import sys
from book_recommender.logging.log import logger
from book_recommender.exception.exception_handler import AppException
from book_recommender.config.configuration import AppConfiguration
import urllib.request
import zipfile

class DataIngestion:
    def __init__(self, app_config=AppConfiguration()):
        """
        DataIngestion Initialization
        data_ingestion_config : DataIngestionConfig
        """
        try:
            logger.info(f"{"="*20} Data Ingestion Started {"="*20}")
            self.data_ingestion_config = app_config.get_data_ingestion_config()
        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e
        
    def download_data(self):
        """
        Fetch the data from the url
        """
        try:
            dataset_url = self.data_ingestion_config.dataset_download_url
            zip_download_dir = self.data_ingestion_config.raw_data_dir
            os.makedirs(zip_download_dir, exist_ok=True)
            data_filename = os.path.basename(dataset_url)
            zip_file_path = os.path.join(zip_download_dir, data_filename)
            logger.info(f"Downloading dataset from {dataset_url} into file {zip_file_path}")
            urllib.request.urlretrieve(dataset_url, zip_file_path)
            logger.info(f"Downloaded dataset from {dataset_url} into {zip_file_path}")
            return zip_file_path
        
        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e
        
    def extract_zip_file(self, zip_file_path: str):
        """
        zip_file_path: str
        Extracts the zip file into raw data directory
        Function returns None
        """
        try:
            ingested_dir = self.data_ingestion_config.ingested_dir
            os.makedirs(ingested_dir, exist_ok=True)
            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                zip_ref.extractall(ingested_dir)
            logger.info(f"extracting zip file: {zip_file_path} into dir: {ingested_dir}")
        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e
        
    def initiate_data_ingestion(self):
        try:
            zip_file_path = self.download_data()
            self.extract_zip_file(zip_file_path=zip_file_path)
            logger.info(f"{"="*20} Data Ingestion Completed {"="*20}")
        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e