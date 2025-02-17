# Memory Search App

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-v2.x-brightgreen)
![FAISS](https://img.shields.io/badge/FAISS-1.7.2-orange)
![SentenceTransformer](https://img.shields.io/badge/SentenceTransformer-all--MiniLM--L6--v2-lightgrey)

Welcome to the **Memory Search App** – a semantic memory engine that leverages cutting-edge machine learning to store, search, and retrieve text data with ease. This project combines the simplicity of Flask, the power of FAISS for efficient similarity searches, and the versatility of Sentence Transformers to encode text into meaningful embeddings.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
  - [Adding Text to Memory](#adding-text-to-memory)
  - [Searching Memory](#searching-memory)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Memory Search App is designed to:
- **Store**: Save textual data and its corresponding embedding into an SQLite database.
- **Index**: Use FAISS to index embeddings for rapid similarity search.
- **Search**: Retrieve the most relevant pieces of text based on semantic similarity to a given query.

This combination allows you to build applications such as chatbots, recommendation systems, or any service that benefits from semantic search.

## Features

- **Real-time Embedding Generation**: Convert text into embeddings using the [Sentence Transformers](https://www.sbert.net/) model.
- **Efficient Search**: Leverage FAISS for lightning-fast similarity searches.
- **Persistent Memory**: Use SQLite to ensure your data is stored persistently.
- **Scalable Mapping**: Seamlessly map between SQLite IDs and FAISS indices for accurate retrieval.

## Technologies

- **[Python](https://www.python.org/)**: Programming language.
- **[Flask](https://flask.palletsprojects.com/)**: Web framework.
- **[SQLite](https://www.sqlite.org/)**: Lightweight relational database.
- **[FAISS](https://github.com/facebookresearch/faiss)**: Library for efficient similarity search.
- **[Sentence Transformers](https://www.sbert.net/)**: Library for creating sentence embeddings.
- **[NumPy](https://numpy.org/)**: For numerical operations.

## Installation

**Clone the repository:**
```bash
git clone https://github.com/datastudy-nl/semantic-search-for-gpt
cd semantic-search-for-gpt
```

## Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```
Install the dependencies:

```bash
pip install -r requirements.txt
```
If you don't have a requirements.txt, here’s a sample:

```text
Flask
faiss-cpu
sentence-transformers
numpy
``` 
## Run the Flask application:

```bash
Copy
python app.py
```
The app will run on http://0.0.0.0:5000.

# Usage
Adding Text to Memory
Send a POST request to /add with a JSON payload containing the text you want to store:

```bash
curl -X POST http://localhost:5000/add \
     -H "Content-Type: application/json" \
     -d '{"text": "Your sample text here."}'
```
## Searching Memory
Send a POST request to /search with your query:

```bash
curl -X POST http://localhost:5000/search \
     -H "Content-Type: application/json" \
     -d '{"query": "search term", "top_k": 5}'
```
The endpoint returns a list of texts ordered by semantic relevance to your query.

## How It Works
 - Text Ingestion: When you add text, the app generates an embedding using the Sentence Transformer model and stores both the text and its embedding in an SQLite database.
- Indexing: The embedding is added to a FAISS index for fast similarity searches.
- Searching: When a search query is submitted, its embedding is computed and compared against all stored embeddings using FAISS. The app then retrieves and returns the most relevant text entries from SQLite.

# Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to enhance the functionality or add new features.

1. Fork the repository.
2. Create your feature branch: git checkout -b feature/my-new-feature
3. Commit your changes: git commit -am 'Add some feature'
4. Push to the branch: git push origin feature/my-new-feature
5. Open a pull request.