# 📚 End-to-End Book Recommender System

A modular, scalable book recommender system built with Python and Streamlit that enables users to get book suggestions using collaborative filtering. It supports training from scratch or using pretrained models for faster loading.

---

## 📦 Project Structure

```
book_recommender/
│
├── components/
│   ├── data_ingestion.py
│   ├── data_validation.py
│   ├── data_transformation.py
│   └── model_trainer.py
│
├── config/
│   └── configuration.py
│
├── constant/
│   └── __init__.py
│
├── entity/
│   ├── config_entity.py
│
├── exception/
│   └── exception_handler.py
│
├── logging/
│   └── log.py
│
├── pipeline/
│   └── training_pipeline.py
│
├── utils/
│   └── util.py
│
├── app.py              # Streamlit UI
├── main.py             # Entry point to run pipeline
├── Dockerfile
├── .dockerignore
└── setup.py
```

Additional directories:

- **artifacts/**: Automatically created by `main.py`  
  ├── `trained_model/`, `ingested_data/`, `raw_data/`, `transformed_data/`  
  └── `serialized_objects/`: Contains pickled model/data

- **logs/**: Auto-created on each run. Stores execution logs.

- **pretrained_objects/**: Contains pre-trained serialized objects (models/data) to skip training phase.

---

## 🚀 Getting Started

### 🔁 Clone this Repository

```bash
git clone https://github.com/kapcodeO/Book-Recommender-System.git
cd book-recommender
```

### 🧱 Set Up Virtual Environment

#### 🔵 macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 🟣 Windows (CMD)

```cmd
python -m venv venv
venv\Scripts\activate
```

> To deactivate:
```bash
deactivate
```

---

## ⚡ Quick Start (Using Pretrained Models)

Once your environment is ready:

```bash
streamlit run app.py
```

This launches the Streamlit web app using pre-trained models from `pretrained_objects/` directory.

---

## 🔬 Train the Model Yourself

If you'd like to train everything from scratch:

```bash
python main.py
```

This will:
- Download data
- Ingest and validate data
- Transform data
- Train model
- Save artifacts in `/artifacts`

---

## 📊 Project Workflow Overview

### 0. Initial Research
Conducted in `research.ipynb`.

---

### 1. Set Constants
In `constant/__init__.py`:
```python
CONFIG_FILE_PATH = os.path.join(os.getcwd(), "config.yaml")
```

---

### 2. Define YAML Configuration (`config.yaml`)
```yaml pseudo code
artifacts_config:
  artifacts_dir: artifacts

data_ingestion_config:
  dataset_download_url: "https://github.com/kapcodeO/asset-strore/raw/refs/heads/main/book_data.zip"
  dataset_dir: dataset
  ingested_data_dir: ingested_data
  raw_data_dir: raw_data

data_validation_config:
  clean_data_dir: clean_data
  serialized_objects_dir: serialized_objects
  books_csv_file: books.csv
  ratings_csv_file: ratings.csv
```

---

### 3. Define Data Classes in `config_entity.py`

```python
DataIngestionConfig = namedtuple("DatasetConfig", [...])
DataValidationConfig = namedtuple("DataValidationConfig", [...])
DataTransformationConfig = namedtuple("DataTransformationConfig", [...])
ModelTrainerConfig = namedtuple("ModelTrainerConfig", [...])
ModelRecommendationConfig = namedtuple("ModelRecommendationConfig", [...])
```

---

### 4. Implement Configuration Logic (`configuration.py`)
Uses:
- `read_yaml_file()`
- Custom `AppException`
- Custom `logger`

```python
class AppConfiguration:
    def get_data_ingestion_config()
    def get_data_validation_config()
    ...
```

---

### 5. Develop Pipeline Components
Each stage like:
- `data_ingestion.py`
- `data_validation.py`
- `data_transformation.py`
- `model_trainer.py`

contains an `initiate_` method to handle specific phases.

---

### 6. Orchestrate via `training_pipeline.py`

```python
class TrainingPipeline:
    def start_training_pipeline():
        self.data_ingestion.initiate_data_ingestion()
        ...
```

---

### 7. Entry Point (`main.py`)
```python
from book_recommender.pipeline.training_pipeline import TrainingPipeline

pipeline = TrainingPipeline()
pipeline.start_training_pipeline()
```

---

### 8. Frontend (`app.py`)
Streamlit-powered interface to interact with recommendation system:
- Loads pretrained objects
- Suggests books based on input

---

## 🐳 Docker (Optional)

Build image:
```bash
docker build -t book-recommender .
```

Run container:
```bash
docker run -p 8501:8501 book-recommender
```

---

## 📝 Logging
Every script execution logs events in the `logs/` directory.

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas, NumPy, Scikit-learn
- Docker (Optional)

---

## 💡 Author

Kapil Ojha  
📧 [kapilojha.work@gmail.com]  
🔗 [LinkedIn](https://www.linkedin.com/in/kapilojha7/) | [GitHub](https://github.com/kapcodeO)

---

## ⭐️ Show your Support

If you like this project, give it a ⭐️  
Pull requests are welcome!
