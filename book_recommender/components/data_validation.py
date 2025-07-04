import os
import sys
import pickle
import pandas as pd
from book_recommender.logging.log import logger
from book_recommender.config.configuration import AppConfiguration
from book_recommender.exception.exception_handler import AppException

class DataValidation:
    def __init__(self, app_config = AppConfiguration()):
        try:
            logger.info(f"{"="*20} Data Validation Started {"="*20}")
            self.data_validation_config = app_config.get_data_validation_config()
        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e
        
    def preprocess_data(self):
        """
        Preprocess the csv files to get the desired modifications
        """
        try:
            ratings = pd.read_csv(self.data_validation_config.ratings_csv_file, sep=";", on_bad_lines="skip", encoding="utf-8")
            books = pd.read_csv(self.data_validation_config.books_csv_file, sep=";", on_bad_lines="skip", encoding="utf-8")

            logger.info(f"shape of ratings csv file: {ratings.shape}")
            logger.info(f"shape of books csv file: {books.shape}")

            # here image url column is important for the poster so we will keep it
            books.drop(columns=["Image-URL-S", "Image-URL-M"], axis=1, inplace=True)

            # renaming for efficient preprocessing
            books.rename(columns={
                "ISBN" : "isbn",
                "Book-Title" : "title",
                "Book-Author" : "author",
                "Year-Of-Publication" : "year",
                "Publisher" : "publisher",
                "Image-URL-L" : "image-url"
            }, inplace=True)

            ratings.rename(columns={
                "User-ID" : "user_id",
                "ISBN" : "isbn",
                "Book-Rating" : "rating"
            }, inplace=True)

            

        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e