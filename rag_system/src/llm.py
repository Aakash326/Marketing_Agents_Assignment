from langchain_openai import ChatOpenAI
from rag_system.config.config import OPENAI_API_KEY, OPENAI_MODEL_NAME
from rag_system.common.logger import get_logger
from rag_system.common.custom_exception import CustomException

logger = get_logger(__name__)

def load_llm(model_name: str = None, openai_api_key: str = None):
    if model_name is None:
        model_name = OPENAI_MODEL_NAME
    if openai_api_key is None:
        openai_api_key = OPENAI_API_KEY
    try:
        logger.info(f"Loading LLM from OpenAI using model: {model_name}...")

        llm = ChatOpenAI(
            openai_api_key=openai_api_key,
            model_name=model_name,
            max_tokens=256,
        )
        logger.info("LLM loaded successfully from OpenAI.")
        return llm

    except Exception as e:
        error_message = CustomException("Failed to load an LLM from OpenAI", e)
        logger.error(str(error_message))
        return None