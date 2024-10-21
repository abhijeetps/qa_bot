from fastapi import UploadFile, HTTPException
from app.models import QuestionList, AnswerList, Answer, Question, QuestionRequest
from app.services.document_loader import DocumentLoader
from app.services.vector_store import VectorStore
from app.services.qa_chain import QAChain
from typing import List, Union
import json

class DocumentProcessor:
    def __init__(self, vector_store: VectorStore, qa_chain: QAChain):
        self.vector_store = vector_store
        self.qa_chain = qa_chain

    async def process_document(self, file: UploadFile) -> str:
        try:
            contents = await file.read()
            file_path = f"/tmp/{file.filename}"
            with open(file_path, "wb") as f:
                f.write(contents)

            documents = DocumentLoader.load_and_split(file_path)
            self.vector_store.create_vector_store(documents)
            return file_path
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

    async def process_questions(self, file: Union[UploadFile, None] = None, questions: Union[QuestionRequest, None] = None) -> List[Question]:
        try:
            if file:
                contents = await file.read()
                questions_data = json.loads(contents.decode())
                return QuestionList(**questions_data).questions
            elif questions:
                return questions.questions
            else:
                raise ValueError("Either file or questions must be provided")
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON format in questions file")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing questions: {str(e)}")

    async def answer_questions(self, questions: List[Question]) -> AnswerList:
        try:
            self.vector_store.load_vector_store()
            answers = []

            for question in questions:
                answer = self.qa_chain.answer_question(question.text)
                answers.append(Answer(question=question.text, answer=answer))

            return AnswerList(answers=answers)
        except FileNotFoundError:
            raise HTTPException(status_code=400, detail="Vector store not found. Please upload a document first.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error answering questions: {str(e)}")
