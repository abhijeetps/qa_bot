import json
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_process_document_and_questions_success(mocker):
    mocker.patch('app.services.document_processor.DocumentProcessor.process_document', return_value=None)
    mocker.patch('app.services.document_processor.DocumentProcessor.process_questions', return_value=["What is AI?", "Define ML."])
    mocker.patch('app.services.document_processor.DocumentProcessor.answer_questions', return_value={"answers": [{"question": "What is AI?", "answer": "AI is Artificial Intelligence."}, {"question": "Define ML.", "answer": "ML stands for Machine Learning."}]})

    response = client.post(
        "/process_document_and_questions",
        files={
            "document": ("test_document.txt", b"Sample content for testing."),
            "questions": ("questions.txt", b"What is AI?\nDefine ML.")
        }
    )
    assert response.status_code == 200
    assert len(response.json()["answers"]) == 2
    assert response.json()["answers"][0]["answer"] == "AI is Artificial Intelligence."

def test_process_document_and_questions_invalid_document():
    response = client.post(
        "/process_document_and_questions",
        files={
            "document": ("test_document.exe", b"Invalid format content."),
            "questions": ("questions.txt", b"What is AI?")
        }
    )
    assert response.status_code == 500

def test_process_document_and_answer_success(mocker):
    mocker.patch('app.services.document_processor.DocumentProcessor.process_document', return_value=None)
    mocker.patch('app.services.document_processor.DocumentProcessor.answer_questions', return_value={"answers": [{"question": "What is AI?", "answer": "AI is Artificial Intelligence."}, {"question": "Define ML.", "answer": "ML stands for Machine Learning."}]})

    questions_json = json.dumps({"questions": [{"text": "What is AI?"}, {"text": "Define ML."}]})

    response = client.post(
        "/process_document_and_answer",
        files={"document": ("test_document.txt", b"Sample content for testing.")},
        data={"questions_json": questions_json}
    )
    assert response.status_code == 200
    assert len(response.json()["answers"]) == 2
    assert response.json()["answers"][0]["answer"] == "AI is Artificial Intelligence."

def test_process_document_and_answer_invalid_json():
    response = client.post(
        "/process_document_and_answer",
        files={"document": ("test_document.txt", b"Sample content for testing.")},
        data={"questions_json": "Not a JSON format."}
    )
    assert response.status_code == 500
    assert response.json()["detail"] == "Error processing document: An error occurred while loading the document: Unsupported file type. Please provide a PDF or JSON file."

def test_process_document_and_answer_unexpected_error(mocker):
    mocker.patch('app.services.document_processor.DocumentProcessor.process_document', side_effect=Exception("Unexpected error"))

    questions_json = json.dumps({"questions": [{"text": "What is AI?"}]})

    response = client.post(
        "/process_document_and_answer",
        files={"document": ("test_document.txt", b"Sample content for testing.")},
        data={"questions_json": questions_json}
    )
    assert response.status_code == 500
    assert "An unexpected error occurred" in response.json()["detail"]
