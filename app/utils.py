import json
from typing import List, Dict
from app.models import Question, QuestionList

from app.config import get_logger

logger = get_logger(__name__)

def load_questions_from_json(file_path: str) -> List[Question]:
    logger.info(f"Loading questions from JSON file: {file_path}")
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        questions = QuestionList(**data)
        logger.debug(f"Loaded {len(questions.questions)} questions")
        return questions.questions
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON format in file: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading questions from {file_path}: {str(e)}")
        raise

def load_json_document(file_path: str) -> Dict:
    logger.info(f"Loading JSON document: {file_path}")
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        logger.debug("JSON document loaded successfully")
        return data
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON format in file: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading JSON document from {file_path}: {str(e)}")
        raise
