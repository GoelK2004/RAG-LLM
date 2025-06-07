# LLM-Powered Document API (RAG System)

This project implements a Retrieval-Augmented Generation (RAG) pipeline for document-based question answering, powered by:

- **FAISS** for vector search
- **SentenceTransformer** for local text embeddings
- Support for `.pdf`, `.docx`, and `.txt` documents
- **Local LLM** (via Hugging Face)
- **Flask REST API** for interaction
- **Dockerized setup** for easy deployment

---

## i. Setup & Installation

### Local Setup (No Docker)

```bash
git clone https://github.com/GoelK2004/RAG-LLM.git
cd RAG-LLM

# Create virtual environment
python -m venv venv
source venv/bin/activate  # (UNIX)
source venv\Scripts\activate #(Windows)

# Install Python dependencies
pip install -r requirements.txt

# Set Hugging Face token
cp .env.example .env
# Edit `.env` to insert your HF_TOKEN

# Run the app
python main.py
```

---

##  ii. Docker Setup

### Step 1: (Optional) Pre-download torch to avoid large downloads during Docker build:

```bash
pip download torch==2.1.2 --python-version 3.10 --only-binary=:all: -d torch_whl
```

### Step 2: Build and Run the Docker App

```bash
docker-compose up --build
```
Access the app at: http://localhost:5000

---

## ii. API Usage & Testing

### Available Endpoints

| Method | Endpoint            | Description                     |
|--------|---------------------|---------------------------------|
|POST 	 |	``` /upload/ ```   | Upload documents for indexing   |
|POST 	 |	``` /query/ ```    | Ask questions to the RAG system |
|GET  	 |	``` /metadata/ ``` | View uploaded document metadata |

### Upload Endpoint – /upload/
POST multipart/form-data

```bash
curl -X POST http://localhost:5000/upload/ \
  -F "files=@sample.txt"
```

Response:
```json
{
  "Response": [
    {
      "filename": "sample.txt",
      "status": "Success",
      "chunks": 6
    }
  ]
}
```

### Query Endpoint – /query/
POST application/json

```json
{
  "question": "What is LangChain?"
}
```

Response:
```json
{
  "Question": "What is LangChain?",
  "Answer": "LangChain is an open-source Python framework...",
  "source_chunks": [...]
}
```

### Metadata Endpoint – /metadata/
GET Returns document metadata:
No Body required

```json
[
  {
    "Chunks": 6,
    "Pages": 1,
    "Filename": "sample.txt",
    "Time": "2025-06-05 15:00"
  }
]
```

### Run Tests
Run all tests:

```bash
pytest
```
---

## iii. Configuration – Using .env File

### Create a .env file in the root directory:
Edit the values as needed:

```env
# Hugging Face token
HF_TOKEN=your_hf_token_here
```

```python
from dotenv import load_dotenv
import os

load_dotenv()
os.getenv("HF_TOKEN")
```

---

## iv. Project Structure

```graphql
.
├── main.py
├── wsgi.py
├── app/
│   ├── api/
│   ├── core/
|   |── db/
|   |── text/
│   └── utils/
├── vector_db/
├── metadata_db/
├── tests/
│   ├── conftest.py
│   ├── test_metadata.py
│   ├── test_query.py
│   └── test_upload.py
├── torch_whl/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
```