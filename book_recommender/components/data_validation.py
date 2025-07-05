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
            self.data_validation_config = app_config.get_data_validation_config()
        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e
        
    def preprocess_data(self):
        """
        Preprocess the csv files to get the desired modifications
        """
        try:
            ratings = pd.read_csv(self.data_validation_config.ratings_csv_file, sep=";", on_bad_lines="skip", encoding="latin-1")
            books = pd.read_csv(self.data_validation_config.books_csv_file, sep=";", on_bad_lines="skip", encoding="latin-1", low_memory=False)

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

            # store users who have rated atleast 200 books
            x = ratings["user_id"].value_counts() >= 200
            y = x[x].index
            ratings = ratings[ratings["user_id"].isin(y)]

            # joining ratings with books
            ratings_with_books = ratings.merge(books, on="isbn")
            total_ratings = ratings_with_books.groupby("title")["rating"].count().reset_index()
            total_ratings = total_ratings.rename(columns={"rating" : "total_ratings"})
            books_with_ratings = ratings_with_books.merge(total_ratings, on="title")

            # books which have minimum 50 or more ratings
            final_ratings = books_with_ratings[books_with_ratings["total_ratings"] >= 50]

            # drop duplicate rows
            final_ratings = final_ratings.drop_duplicates(["user_id", "title"])
            logger.info(f"Shape of final cleaned dataset: {final_ratings.shape}")

            # saving the cleaned data for transformations
            os.makedirs(self.data_validation_config.clean_data_dir, exist_ok=True)
            final_ratings.to_csv(os.path.join(self.data_validation_config.clean_data_dir, "clean_data.csv"), index=False)
            logger.info(f"Saved clean_data.csv into : {self.data_validation_config.clean_data_dir}")

            # saving final_ratings object for web app
            os.makedirs(self.data_validation_config.serialized_objects_dir, exist_ok=True)
            pickle.dump(final_ratings, open(os.path.join(self.data_validation_config.serialized_objects_dir, "final_ratings.pkl"), "wb"))
            logger.info(f"Saved final_ratings.pkl file to {self.data_validation_config.serialized_objects_dir}")

        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e
        
    def initiate_data_validation(self):
        try:
            logger.info(f"{"="*20} Data Validation Started {"="*20}")
            self.preprocess_data()
            logger.info(f"{"="*20} Data Validation Completed {"="*20}")
        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e