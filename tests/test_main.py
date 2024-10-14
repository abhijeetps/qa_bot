import json
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_document_success(mocker):
    mocker.patch('app.services.document_loader.DocumentLoader.load_and_split', return_value=["doc1", "doc2"])
    mocker.patch('app.services.vector_store.VectorStore.create_vector_store', return_value=None)

    response = client.post(
        "/upload_document",
        files={"file": ("test_document.txt", b"Sample content for testing.")}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Document uploaded and processed successfully"}

def test_upload_document_invalid_format():
    response = client.post(
        "/upload_document",
        files={"file": ("test_document.exe", b"Invalid format content.")}
    )
    assert response.status_code == 500  # Adjust based on your exception handling

def test_answer_questions_success(mocker):
    mock_questions = json.dumps({"questions": [{"text": "What is AI?"}, {"text": "Define ML."}]})
    mocker.patch('app.services.vector_store.VectorStore.load_vector_store', return_value=None)
    mocker.patch('app.services.qa_chain.QAChain.answer_question', side_effect=["AI is Artificial Intelligence.", "ML stands for Machine Learning."])

    response = client.post(
        "/answer_questions",
        files={"file": ("questions.json", mock_questions.encode())}
    )
    assert response.status_code == 200
    assert len(response.json()["answers"]) == 2
    assert response.json()["answers"][0]["answer"] == "AI is Artificial Intelligence."

def test_answer_questions_invalid_json():
    response = client.post(
        "/answer_questions",
        files={"file": ("invalid_questions.txt", b"Not a JSON format.")}
    )
    assert response.status_code == 500  # Adjust based on your exception handling

def test_answer_questions_empty_vector_store(mocker):
    mocker.patch('app.services.vector_store.VectorStore.load_vector_store', side_effect=Exception("Vector store not loaded."))

    mock_questions = json.dumps({"questions": [{"text": "What is AI?"}]})

    response = client.post(
        "/answer_questions",
        files={"file": ("questions.json", mock_questions.encode())}
    )
    assert response.status_code == 500  # Adjust based on your exception handling
