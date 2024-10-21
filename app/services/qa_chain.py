from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from app.config import OPENAI_API_KEY, MODEL_NAME
from app.services.vector_store import VectorStore

from app.config import get_logger

logger = get_logger(__name__)

class QAChain:
    def __init__(self, vector_store: VectorStore):
        logger.info("Initializing QAChain")
        self.llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name=MODEL_NAME)
        self.vector_store = vector_store
        self.qa_chain = None

    def initialize_qa_chain(self):
        logger.info("Initializing QA chain")
        retriever = self.vector_store.get_retriever()
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )
        logger.debug("QA chain initialized successfully")

    def answer_question(self, question: str) -> str:
        logger.info(f"Answering question: {question}")
        if not self.qa_chain:
            logger.debug("QA chain not initialized. Initializing now.")
            self.initialize_qa_chain()
        result = self.qa_chain({"query": question})
        logger.debug("Question answered successfully")
        return result["result"]
