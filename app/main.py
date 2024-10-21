from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from app.models import QuestionRequest
from app.services.vector_store import VectorStore
from app.services.qa_chain import QAChain
from app.services.document_processor import DocumentProcessor
import uvicorn
import json

from app.config import get_logger

logger = get_logger(__name__)

app = FastAPI()

vector_store = VectorStore()
qa_chain = QAChain(vector_store)
document_processor = DocumentProcessor(vector_store, qa_chain)

@app.post("/process_document_and_questions")
async def process_document_and_questions(
    document: UploadFile = File(...),
    questions: UploadFile = File(...)
):
    logger.info(f"Processing document: {document.filename} and questions file")
    try:
        await document_processor.process_document(document)
        questions_list = await document_processor.process_questions(file=questions)
        logger.info("Document and questions processed successfully")
        return await document_processor.answer_questions(questions_list)
    except HTTPException as he:
        logger.error(f"HTTP exception occurred: {str(he)}")
        raise he
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.post("/process_document_and_answer")
async def process_document_and_answer(
    document: UploadFile = File(...),
    questions_json: str = Form(...)
):
    logger.info(f"Processing document: {document.filename} and JSON questions")
    try:
        await document_processor.process_document(document)
        questions_data = json.loads(questions_json)
        questions = QuestionRequest(**questions_data)
        logger.info("Document processed and questions parsed successfully")
        return await document_processor.answer_questions(questions.questions)
    except json.JSONDecodeError:
        logger.error("Invalid JSON format for questions")
        raise HTTPException(status_code=400, detail="Invalid JSON format for questions")
    except HTTPException as he:
        logger.error(f"HTTP exception occurred: {str(he)}")
        raise he
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    logger.info("Starting the application")
    uvicorn.run(app, host="0.0.0.0", port=8000)
