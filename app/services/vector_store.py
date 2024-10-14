from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from typing import List
from langchain.schema import Document
from app.config import OPENAI_API_KEY, VECTOR_STORE_PATH
import os

class VectorStore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        self.vector_store = None

    def create_vector_store(self, documents: List[Document]):
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        self.vector_store.save_local(VECTOR_STORE_PATH)

    def load_vector_store(self):
        if os.path.exists(VECTOR_STORE_PATH):
            self.vector_store = FAISS.load_local(VECTOR_STORE_PATH, self.embeddings)
        else:
            raise FileNotFoundError(f"Vector store not found at {VECTOR_STORE_PATH}. Please upload a document first.")

    def similarity_search(self, query: str, k: int = 4):
        if not self.vector_store:
            self.load_vector_store()
        return self.vector_store.similarity_search(query, k=k)

    def get_retriever(self, search_kwargs=None):
        if not self.vector_store:
            self.load_vector_store()
        return self.vector_store.as_retriever(search_kwargs=search_kwargs or {"k": 4})
