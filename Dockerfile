# Base Image
FROM python:3.12-slim

# Because streamlit works on localhost::8501
EXPOSE 8501

# Install System Dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf var/lib/apt/lists/*

# Specify working directory
WORKDIR /app

# Copy source code of app to the working directory
COPY . /app

# Install requirements
RUN pip3 install -r requirements.txt

# Specify Entrypoint
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]