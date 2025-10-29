import os
from rag_system.src.document_processor import load_all_documents, create_text_chunks
from rag_system.src.vector_store import save_vector_store
from rag_system.config.config import DB_FAISS_PATH
from rag_system.common.logger import get_logger
from rag_system.common.custom_exception import CustomException

logger = get_logger(__name__)

def process_and_store_documents():
    """Load all documents (PDF + TXT) and create vector store"""
    try:
        logger.info("=" * 80)
        logger.info("Creating RAG Vector Store")
        logger.info("=" * 80)

        # Load all documents
        documents = load_all_documents()

        if not documents:
            logger.error("No documents found! Cannot create vector store.")
            return False

        # Create chunks
        text_chunks = create_text_chunks(documents)

        if not text_chunks:
            logger.error("Failed to create text chunks")
            return False

        # Save to vector store
        db = save_vector_store(text_chunks)

        if db:
            logger.info("=" * 80)
            logger.info("Vector store created successfully!")
            logger.info(f"Documents: {len(documents)}")
            logger.info(f"Chunks: {len(text_chunks)}")
            logger.info(f"Saved to: {DB_FAISS_PATH}")
            logger.info("=" * 80)
            return True
        else:
            logger.error("Failed to save vector store")
            return False

    except Exception as e:
        error_message = CustomException("Failed to create vectorstore", e)
        logger.error(str(error_message))
        return False


if __name__ == "__main__":
    success = process_and_store_documents()
    exit(0 if success else 1)
