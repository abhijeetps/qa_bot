from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from typing import List
from langchain.schema import Document
from app.config import OPENAI_API_KEY, VECTOR_STORE_PATH
import os

from app.config import get_logger

logger = get_logger(__name__)

class VectorStore:
    def __init__(self):
        logger.info("Initializing VectorStore")
        self.embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        self.vector_store = None

    def create_vector_store(self, documents: List[Document]):
        logger.info(f"Creating vector store with {len(documents)} documents")
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        self.vector_store.save_local(VECTOR_STORE_PATH)
        logger.debug(f"Vector store saved to {VECTOR_STORE_PATH}")

    def load_vector_store(self):
        logger.info(f"Loading vector store from {VECTOR_STORE_PATH}")
        try:
            self.vector_store = FAISS.load_local(VECTOR_STORE_PATH, self.embeddings)
            logger.debug("Vector store loaded successfully")
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            raise FileNotFoundError(f"Vector store not found at {VECTOR_STORE_PATH}. Please upload a document first.")

    def similarity_search(self, query: str, k: int = 4):
        logger.info(f"Performing similarity search for query: {query}")
        if not self.vector_store:
            logger.debug("Vector store not loaded. Loading now.")
            self.load_vector_store()
        results = self.vector_store.similarity_search(query, k=k)
        logger.debug(f"Found {len(results)} similar documents")
        return results

    def get_retriever(self, search_kwargs=None):
        logger.info("Getting retriever")
        if not self.vector_store:
            logger.debug("Vector store not loaded. Loading now.")
            self.load_vector_store()
        retriever = self.vector_store.as_retriever(search_kwargs=search_kwargs or {"k": 4})
        logger.debug("Retriever created successfully")
        return retriever
