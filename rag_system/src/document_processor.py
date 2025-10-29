"""
Document Processor - Loads both TXT and PDF files for RAG system
"""
import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from rag_system.common.logger import get_logger
from rag_system.common.custom_exception import CustomException
from rag_system.config.config import CHUNK_SIZE, CHUNK_OVERLAP

logger = get_logger(__name__)

# Paths for both PDF and TXT documents
PDF_PATH = "./rag_system/knowledge_base/raw_documents"
TXT_PATH = "./rag_system/data_sources/raw_documents"


def load_all_documents():
    """Load both PDF and TXT files"""
    all_documents = []

    try:
        # Load PDFs if they exist
        if os.path.exists(PDF_PATH):
            logger.info(f"Loading PDFs from {PDF_PATH}")
            pdf_loader = DirectoryLoader(PDF_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
            pdf_docs = pdf_loader.load()
            if pdf_docs:
                all_documents.extend(pdf_docs)
                logger.info(f"✅ Loaded {len(pdf_docs)} PDF documents")
            else:
                logger.info("No PDFs found")

        # Load TXT files if they exist
        if os.path.exists(TXT_PATH):
            logger.info(f"Loading TXT files from {TXT_PATH}")
            txt_loader = DirectoryLoader(TXT_PATH, glob="*.txt", loader_cls=TextLoader)
            txt_docs = txt_loader.load()
            if txt_docs:
                all_documents.extend(txt_docs)
                logger.info(f"✅ Loaded {len(txt_docs)} TXT documents")
            else:
                logger.info("No TXT files found")

        if not all_documents:
            logger.warning("⚠️  No documents found in either directory")
            logger.info(f"Please add files to:")
            logger.info(f"  - PDFs: {PDF_PATH}")
            logger.info(f"  - TXT: {TXT_PATH}")
        else:
            logger.info(f"📚 Total documents loaded: {len(all_documents)}")

        return all_documents

    except Exception as e:
        error_message = CustomException("Failed to load documents", e)
        logger.error(str(error_message))
        return []


def create_text_chunks(documents):
    """Split documents into chunks"""
    try:
        if not documents:
            raise CustomException("No documents were found")

        logger.info(f"Splitting {len(documents)} documents into chunks")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

        text_chunks = text_splitter.split_documents(documents)

        logger.info(f"✅ Generated {len(text_chunks)} text chunks")
        return text_chunks

    except Exception as e:
        error_message = CustomException("Failed to generate chunks", e)
        logger.error(str(error_message))
        return []


if __name__ == "__main__":
    print("=" * 80)
    print("Testing Document Processor")
    print("=" * 80)

    docs = load_all_documents()
    print(f"\nLoaded {len(docs)} documents")

    if docs:
        chunks = create_text_chunks(docs)
        print(f"Created {len(chunks)} chunks")
        print(f"\nSample chunk:")
        print("-" * 80)
        print(chunks[0].page_content[:200] + "...")

    print("=" * 80)
