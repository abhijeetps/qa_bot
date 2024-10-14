from fastapi import FastAPI, UploadFile, File, HTTPException
from app.models import QuestionList, AnswerList, Answer
from app.services.document_loader import DocumentLoader
from app.services.vector_store import VectorStore
from app.services.qa_chain import QAChain
from app.utils import load_questions_from_json
import json

import uvicorn

app = FastAPI()

vector_store = VectorStore()
qa_chain = QAChain(vector_store)

@app.post("/upload_document") 
async def upload_document(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        with open(file.filename, "wb") as f:
            f.write(contents)

        documents = DocumentLoader.load_and_split(file.filename)
        vector_store.create_vector_store(documents)
        return {"message": "Document uploaded and processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/answer_questions")
async def answer_questions(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        questions = json.loads(contents.decode())
        question_list = QuestionList(**questions)

        # Ensure the vector store is loaded before answering questions
        vector_store.load_vector_store()

        answers = []

        for question in question_list.questions:
            answer = qa_chain.answer_question(question.text)
            answers.append(Answer(question=question.text, answer=answer))

        return AnswerList(answers=answers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
