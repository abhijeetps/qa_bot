from langchain.document_loaders import PyPDFLoader, JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document

from app.config import get_logger

logger = get_logger(__name__)

class DocumentLoader:
    @staticmethod
    def load_and_split(file_path: str) -> List[Document]:
        logger.info(f"Loading and splitting document: {file_path}")
        documents = []

        try:
            if file_path.endswith('.pdf'):
                logger.debug("Loading PDF document")
                loader = PyPDFLoader(file_path)
                documents = loader.load()
            elif file_path.endswith('.json'):
                logger.debug("Loading JSON document")
                loader = JSONLoader(
                    file_path=file_path,
                    jq_schema='.content',
                    text_content=True
                )
                documents = loader.load()
            else:
                logger.error(f"Unsupported file type: {file_path}")
                raise ValueError("Unsupported file type. Please provide a PDF or JSON file.")

            logger.debug(f"Loaded {len(documents)} document(s)")

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            split_docs = text_splitter.split_documents(documents)
            logger.info(f"Document split into {len(split_docs)} chunks")
            return split_docs

        except Exception as e:
            logger.error(f"An error occurred while loading the document: {e}")
            raise RuntimeError(f"An error occurred while loading the document: {e}")
