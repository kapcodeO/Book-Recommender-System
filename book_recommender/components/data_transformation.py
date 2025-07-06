# STAGE 3

import os
import sys
import pickle
import pandas as pd
from book_recommender.config.configuration import AppConfiguration
from book_recommender.logging.log import logger
from book_recommender.exception.exception_handler import AppException

class DataTransformation:
    def __init__(self, app_config = AppConfiguration()):
        try:
            self.data_transformation_config = app_config.get_data_transformation_config()
            self.data_validation_config = app_config.get_data_validation_config()
        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e
        
    def get_data_transformer(self):
        """
        Transforms the final data into pivot table for collaborative filtering
        """
        try:
            df = pd.read_csv(os.path.join(self.data_validation_config.clean_data_dir, "clean_data.csv"))
            
            # create a pivot table
            book_pivot = df.pivot_table(
                index="title",
                columns="user_id",
                values="rating"
            )
            logger.info(f"book_pivot data shape : {book_pivot.shape}")
            book_pivot.fillna(0, inplace=True)

            # save book names
            book_names = book_pivot.index
            logger.info(f"book_names data shape : {book_names.shape}")

            # save book_pivot table data
            os.makedirs(self.data_transformation_config.transformed_data_dir, exist_ok=True)
            pickle.dump(book_pivot, open(os.path.join(self.data_transformation_config.transformed_data_dir, "book_pivot.pkl"), "wb"))
            logger.info(f"Saved book_pivot.pkl to : {self.data_transformation_config.transformed_data_dir}")

            # saving book names for web app
            os.makedirs(self.data_validation_config.serialized_objects_dir, exist_ok=True)
            pickle.dump(book_names, open(os.path.join(self.data_validation_config.serialized_objects_dir, "book_names.pkl"), "wb"))
            logger.info(f"Saved book_names.pkl to: {self.data_validation_config.serialized_objects_dir}")

            # save book_pivot data for web app
            os.makedirs(self.data_validation_config.serialized_objects_dir, exist_ok=True)
            pickle.dump(book_pivot, open(os.path.join(self.data_validation_config.serialized_objects_dir, "book_pivot.pkl"), "wb"))
            logger.info(f"Saved book_pivot.pkl for web app to: {self.data_validation_config.serialized_objects_dir}")

        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e
        
    def initiate_data_transformation(self):
        try:
            logger.info(f"{"="*20} Data Transformation Started {"="*20}")
            self.get_data_transformer()
            logger.info(f"{"="*20} Data Transformation Completed {"="*20}")
        
        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e