from fastapi import UploadFile, HTTPException
from app.models import QuestionList, AnswerList, Answer, Question, QuestionRequest
from app.services.document_loader import DocumentLoader
from app.services.vector_store import VectorStore
from app.services.qa_chain import QAChain
from typing import List, Union
import json

from app.config import get_logger

logger = get_logger(__name__)

class DocumentProcessor:
    def __init__(self, vector_store: VectorStore, qa_chain: QAChain):
        self.vector_store = vector_store
        self.qa_chain = qa_chain

    async def process_document(self, file: UploadFile) -> str:
        logger.info(f"Processing document: {file.filename}")
        try:
            contents = await file.read()
            file_path = f"/tmp/{file.filename}"
            with open(file_path, "wb") as f:
                f.write(contents)

            logger.debug(f"Document saved to {file_path}")
            documents = DocumentLoader.load_and_split(file_path)
            self.vector_store.create_vector_store(documents)
            logger.info("Vector store created successfully")
            return file_path
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

    async def process_questions(self, file: Union[UploadFile, None] = None, questions: Union[QuestionRequest, None] = None) -> List[Question]:
        logger.info("Processing questions")
        try:
            if file:
                contents = await file.read()
                questions_data = json.loads(contents.decode())
                logger.debug("Questions loaded from file")
                return QuestionList(**questions_data).questions
            elif questions:
                logger.debug("Questions provided directly")
                return questions.questions
            else:
                logger.error("No questions provided")
                raise ValueError("Either file or questions must be provided")
        except json.JSONDecodeError:
            logger.error("Invalid JSON format in questions file")
            raise HTTPException(status_code=400, detail="Invalid JSON format in questions file")
        except Exception as e:
            logger.error(f"Error processing questions: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing questions: {str(e)}")

    async def answer_questions(self, questions: List[Question]) -> AnswerList:
        logger.info(f"Answering {len(questions)} questions")
        try:
            self.vector_store.load_vector_store()
            answers = []

            for i, question in enumerate(questions, 1):
                logger.debug(f"Processing question {i}: {question.text}")
                answer = self.qa_chain.answer_question(question.text)
                answers.append(Answer(question=question.text, answer=answer))

            logger.info("All questions answered successfully")
            return AnswerList(answers=answers)
        except FileNotFoundError:
            logger.error("Vector store not found")
            raise HTTPException(status_code=400, detail="Vector store not found. Please upload a document first.")
        except Exception as e:
            logger.error(f"Error answering questions: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error answering questions: {str(e)}")
