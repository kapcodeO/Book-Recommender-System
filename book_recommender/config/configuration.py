import os
import sys
from book_recommender.logging.log import logger
from book_recommender.utils.util import read_yaml_file
from book_recommender.exception.exception_handler import AppException
from book_recommender.entity.config_entity import DataIngestionConfig, DataValidationConfig
from book_recommender.entity.config_entity import DataTransformationConfig, ModelTrainerConfig
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
        
    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            data_ingestion_config = self.configs_info["data_ingestion_config"]
            data_validation_config = self.configs_info["data_validation_config"]
            dataset_dir = data_ingestion_config["dataset_dir"]
            artifacts_dir = self.configs_info["artifacts_config"]["artifacts_dir"]
            books_csv_file = data_validation_config["books_csv_file"]
            ratings_csv_file = data_validation_config["ratings_csv_file"]

            books_csv_file_dir = os.path.join(artifacts_dir, 
                                              dataset_dir, 
                                              data_ingestion_config["ingested_data_dir"],
                                              "books_data", books_csv_file)
            ratings_csv_file_dir = os.path.join(artifacts_dir, 
                                                dataset_dir, 
                                                data_ingestion_config["ingested_data_dir"],
                                                "books_data",
                                                ratings_csv_file)
            clean_data_dir = os.path.join(artifacts_dir, dataset_dir, data_validation_config["clean_data_dir"])
            serialized_objects_dir = os.path.join(artifacts_dir, data_validation_config["serialized_objects_dir"])

            response = DataValidationConfig(
                clean_data_dir = clean_data_dir,
                books_csv_file = books_csv_file_dir,
                ratings_csv_file = ratings_csv_file_dir,
                serialized_objects_dir = serialized_objects_dir
            )
            logger.info(f"Data Validation Config: {response}")
            return response
        
        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e
        
    def get_data_transformation_config(self) -> DataTransformationConfig:
        try:
            data_transformation_config = self.configs_info["data_transformation_config"]
            data_validation_config = self.configs_info["data_validation_config"]
            data_ingestion_config = self.configs_info["data_ingestion_config"]
            dataset_dir = data_ingestion_config["dataset_dir"]
            artifacts_dir = self.configs_info["artifacts_config"]["artifacts_dir"]

            clean_data_dir = os.path.join(artifacts_dir, dataset_dir, data_validation_config["clean_data_dir"], "clean_data.csv")
            transformed_data_dir = os.path.join(artifacts_dir, dataset_dir, data_transformation_config["transformed_data_dir"])

            response = DataTransformationConfig(
                clean_data_dir = clean_data_dir,
                transformed_data_dir = transformed_data_dir
            )
            
            logger.info(f"Data transformation config : {response}")
            return response
        
        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e
        
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        try:
            model_trainer_config = self.configs_info["model_trainer_config"]
            data_transformation_config = self.configs_info["data_transformation_config"]
            dataset_dir = self.configs_info["data_ingestion_config"]["dataset_dir"]
            artifacts_dir = self.configs_info["artifacts_config"]["artifacts_dir"]

            transformed_data_dir = os.path.join(artifacts_dir, dataset_dir, data_transformation_config["transformed_data_dir"])
            trained_model_dir = os.path.join(artifacts_dir, dataset_dir, model_trainer_config["trained_model_dir"])
            trained_model_name = model_trainer_config["trained_model_name"]

            response = ModelTrainerConfig(
                transformed_data_dir = transformed_data_dir,
                trained_model_dir = trained_model_dir,
                trained_model_name = trained_model_name
            )

            logger.info(f"Model Trainer Config: {response}")
            return response
        
        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e