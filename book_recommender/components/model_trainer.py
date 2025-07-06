# STAGE 4

import os
import sys
import pickle 
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from book_recommender.config.configuration import AppConfiguration
from book_recommender.logging.log import logger
from book_recommender.exception.exception_handler import AppException

class ModelTrainer:
    def __init__(self, app_config = AppConfiguration()):
        try:
            self.model_trainer_config = app_config.get_model_trainer_config()
            self.data_transformation_config = app_config.get_data_transformation_config()
        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e
        
    def train(self):
        """
        trains the nearest neighbors model on a csr matrix
        """
        try:
            # load pivot data
            pivot_path = os.path.join(self.data_transformation_config.transformed_data_dir, "book_pivot.pkl")
            logger.info(f"Loading pivot matrix from: {pivot_path}")
            book_pivot = pickle.load(open(pivot_path, "rb"))
            logger.info(f"Type of loaded object: {type(book_pivot)}")
            book_sparse = csr_matrix(book_pivot)

            # train the model
            model = NearestNeighbors(algorithm="brute", metric="cosine")
            model.fit(book_sparse)

            # save model object for recommendations
            os.makedirs(self.model_trainer_config.trained_model_dir, exist_ok=True)
            model_path = os.path.join(self.model_trainer_config.trained_model_dir, self.model_trainer_config.trained_model_name)
            pickle.dump(model, open(model_path, "wb"))
            logger.info(f"Saving final model to : {model_path}")

        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e
        
    def initiate_model_training(self):
        try:
            logger.info(f"{"="*20} Model Training Started {"="*20}")
            self.train()
            logger.info(f"{"="*20} Model Training Completed {"="*20}")

        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e