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

### 📂 Create a Project Folder

```bash
# go to the desired location then open
# powershell or terminal in that folder then run
mkdir book-recommender
cd book-recommender
```

### 🔁 Clone this Repository

```bash
git clone https://github.com/kapcodeO/Book-Recommender-System.git
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

## 🐳 Streamlit App Docker Image Deployment

1. Login with your AWS console and open and EC2 Instance
2. NOTE: these commands are meant to run on EC2 Intance not on local machine
3. NOTE: do the port mapping to -> 8501
4. Run the following commands:

Install Docker:
```bash
sudo apt-get update -y
sudo apt-get upgrade -y

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

Clone you Project:
```bash
git clone "https://github.com/kapcodeO/Book-Recommender-System.git"
cd Book-Recommender-System
```

Build Image:
```bash
docker build -t kapcodeO/book-recommender:latest .
docker images -a
```

Run and Manage Docker Container:
```bash
docker run -d -p 8501:8501 kapcodeO/book-recommender
docker ps
# now your app is running
# just paste the <public ip address>:8501 in any browser
docker stop container_id
docker rm $(docker ps -a -q)
```

Login Docker (for docker hub not needed for AWS):
```bash
docker login
docker push kapcodeO/book-recommender:latest
docker rmi kapcodeO/book-recommender:latest
docker pull kapcodeO/book-recommender
```


### For local machine: 

NOTE: you need to have docker desktop installed on your local machine

Build image:
```bash
docker build -t book-recommender .
```

Run container:
```bash
docker run -d -p 8501:8501 book-recommender
```

To see live logs (optional):
```bash
# To find the container_id
docker ps       
docker logs <container_id>
```


---

## 📝 AWS Deployment

Follow these steps to deploy on AWS :

- Open [AWS](https://aws.amazon.com/) and login .
- Create a account if account doesen't already exists.(will ask for Debit/Credit card and PAN number but it's safe.)
- In the right corner select server `Asia Pacific (Mumbai)`.
- In the Search Tab search for `EC2`.
- Then navigate to `Dashboard` in the top left menu.
- Click on `Launch Instance`.
- Enter the name of your project or instance .
- Select `Ubuntu` as an Application and OS Images.
- Then select `t2.large` instance type.
- ⚠️ NOTE: it will charge you atleast 12Rs per hour.
- Create a new keypair value by clicking on `create new key pair`.
- Select on `.pem` and click the bottom yellow button.
- That will download an ssh certificate to your machine. 
- In `Network Settings` > `Create Security Group` > select all `Allow`options.
- In `Configure Storage` enter `16` instead of `8`.
- Then click on `Launch Instance` located on bottom right side of page.
- After that click on `Instance ID` and Scroll Down and click `Security`.
- Here click on `Security Groups link` > `Edit Inbound Rules`.
- Click on `Add Rule` in the column enter `8501` for streamlit port mapping.
- In the next column enter `0.0.0.0/0` to access from anywhere.
- Click on `Save Changes` then go back to instance and click on `Instance ID`.
- Then click on `Connect` it will launch and `Ubuntu t2.large instance on a remote server`.
- Then run the following `Streamlit App Docker Image Deployment`

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
