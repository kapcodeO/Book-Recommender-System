from setuptools import setup, find_packages

with open("Readme.md", "r", encoding="utf-8") as f:
    long_description = f.read()

## edit below variables as per your requirements
REPO_NAME = "ML Based Book Recommender System"
AUTHOR_NAME = "KAPIL OJHA"
SRC_REPO = "books_recommender"
LIST_OF_REQUIREMENTS = []

setup(
    name=SRC_REPO,
    version="0.0.1",
    author=AUTHOR_NAME, 
    description=REPO_NAME,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kapcodeO/Book-Recommender-System.git"
    author_email="kapilojha953@gmail.com",
    packages=find_packages(),
    license="MIT",
    python_requires=">=3.12",
    install_requires=LIST_OF_REQUREMENTS
)