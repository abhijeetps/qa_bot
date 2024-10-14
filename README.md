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

4. Create a `.env` file in the project root and add your OpenAI API key, Pinecode API Key and Pinecode Environment:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   PINECONE_ENVIRONMENT=your_pinecone_environment_here
   ```

## Running the API

To run the API, use the following command:

```
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Endpoints

1. `/upload_document` (POST): Upload a document (PDF or JSON) for processing.
2. `/answer_questions` (POST): Submit a list of questions to be answered based on the uploaded document.

## Usage

1. Upload a document:

   ```
   curl -X POST -F "file=@path/to/your/document.pdf" http://localhost:8000/upload_document
   ```

2. Submit questions:

   ```
   curl -X POST -F "file=@path/to/your/questions.json" http://localhost:8000/answer_questions
   ```

   The `questions.json` file should have the following format:

   ```json
   {
     "questions": [
       { "text": "What is the capital of France?" },
       { "text": "Who wrote Romeo and Juliet?" }
     ]
   }
   ```

## Running Tests

To run the tests, use the following command:

```
pytest
```
