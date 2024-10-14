from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from app.config import OPENAI_API_KEY, MODEL_NAME
from app.services.vector_store import VectorStore

class QAChain:
    def __init__(self, vector_store: VectorStore):
        self.llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name=MODEL_NAME)
        self.vector_store = vector_store
        self.qa_chain = None

    def initialize_qa_chain(self):
        retriever = self.vector_store.get_retriever()
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )

    def answer_question(self, question: str) -> str:
        if not self.qa_chain:
            self.initialize_qa_chain()
        result = self.qa_chain({"query": question})
        return result["result"]
