from book_recommender.components.data_ingestion import DataIngestion

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()

    def start_training_pipeline(self):
        """
        Starts the training pipeline
        :return : Nonne
        """
        self.data_ingestion.initiate_data_ingestion()