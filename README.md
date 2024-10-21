# Question-Answering Bot API

This project implements a backend API for a Question-Answering bot using the LangChain framework, FastAPI, and OpenAI's GPT-4 model.

## Features

- Supports PDF and JSON input documents
- Uses FAISS for efficient similarity search
- Implements a RESTful API using FastAPI

## Setup

1. Clone the repository:

   ```
   git clone https://github.com/abhijeetps/qa_bot.git
   cd qa_bot
   ```

2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your OpenAI API key:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Running the API

To run the API, use the following command:

```
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Endpoints

1. `/process_document_and_questions` (POST): Upload a document (PDF) and a JSON file with questions for processing.
2. `/process_document_and_answer (POST)`: Upload a document (PDF) and submit questions directly as part of the request payload.


## Usage

1. Upload a document and questions from files:

   ```
   curl -X POST http://localhost:8000/process_document_and_questions \
   -H "Content-Type: multipart/form-data" \
   -F "document=@path/to/your/document.pdf" \
   -F "questions=@path/to/your/questions.json"

   ```

   The _questions.json_ should have the following format:

   ```json
   {
     "questions": [
       { "text": "What is the capital of France?" },
       { "text": "Who wrote Romeo and Juliet?" }
     ]
   }
   ```


2. Upload a document and submit questions directly as JSON:

```

curl -X POST http://localhost:8000/process_document_and_answer \
  -H "Content-Type: multipart/form-data" \
  -F "document=@path/to/your/document.pdf" \
  -F "questions={\"questions\": [{\"text\": \"What is the capital of France?\"}, {\"text\": \"Who wrote Romeo and Juliet?\"}]};type=application/json"

```
In this case, the questions are passed directly as a JSON string in the request.



## Running Tests

To run the tests, use the following command:

```
pytest tests
```
