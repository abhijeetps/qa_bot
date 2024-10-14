from langchain.document_loaders import PyPDFLoader, JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document

class DocumentLoader:
    @staticmethod
    def load_and_split(file_path: str) -> List[Document]:
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
            documents = loader.load()
        elif file_path.endswith('.json'):
            loader = JSONLoader(file_path=file_path, jq_schema='.')
            documents = loader.load()
        else:
            raise ValueError("Unsupported file type. Please provide a PDF or JSON file.")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return text_splitter.split_documents(documents)
