import os
import sys
import pickle
import numpy as np
import streamlit as st
from book_recommender.logging.log import logger
from book_recommender.config.configuration import AppConfiguration
from book_recommender.exception.exception_handler import AppException
from book_recommender.pipeline.training_pipeline import TrainingPipeline

class Recommendation:
    def __init__(self, app_config = AppConfiguration()):
        try:
            self.recommendation_config = app_config.get_recommendation_config()
            self.model_trainer_config = app_config.get_model_trainer_config()
            self.book_names_dir = self.recommendation_config.book_name_serialized_objects
        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e
        
    def fetch_poster(self, suggestion):
        try:
            book_name = []
            ids_index = []
            poster_url = []
            book_pivot = pickle.load(open(self.recommendation_config.book_pivot_serialized_objects, "rb"))
            final_rating = pickle.load(open(self.recommendation_config.final_rating_serialized_objects, "rb"))

            for book_id in suggestion:
                book_name.append(book_pivot.index[book_id])

            for name in book_name[0]:
                ids = np.where(final_rating.title == name)[0][0]
                ids_index.append(ids)

            for idx in ids_index:
                url = final_rating.iloc[idx]["image_url"]
                poster_url.append(url)

            return poster_url
        
        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e
        
    def recommend_book(self, book_name):
        try:
            books_list = []
            model = pickle.load(open(os.path.join(self.model_trainer_config.trained_model_dir, self.model_trainer_config.trained_model_name), "rb"))
            book_pivot = pickle.load(open(self.recommendation_config.book_pivot_serialized_objects, "rb"))
            book_id = np.where(book_pivot.index == book_name)[0][0]
            distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1, -1), n_neighbors=6)
            
            poster_url = self.fetch_poster(suggestion)

            for i in range(len(suggestion[0])):
                books_list.append(book_pivot.index[suggestion[0][i]])
            
            return books_list, poster_url

        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e


    def recommendation_engine(self, selected_books):
        try:
            with st.spinner("Generating recommendations..."):
                recommended_books, poster_urls = self.recommend_book(selected_books)

            st.markdown("---")
            st.subheader("Recommended Books")

            cols = st.columns(5)
            for i in range(1, 6):  # Skip the input book (index 0)
                with cols[i - 1]:
                    st.image(poster_urls[i], caption=recommended_books[i])

        except Exception as e:
            logger.error(e)
            raise AppException(e, sys) from e


if __name__ == "__main__":
    st.set_page_config(page_title="Book Recommender", layout='centered')

    st.markdown("# Book Recommender System 📚")
    st.caption("Find your next favorite read using collaborative filtering")

    obj = Recommendation()
    book_names = pickle.load(open(obj.book_names_dir, "rb"))

    selected_books = st.selectbox(
        "Select a book you like:",
        book_names,
        index=0
    )

    if st.button("🚀  Recommend Books"):
        obj.recommendation_engine(selected_books=selected_books)
