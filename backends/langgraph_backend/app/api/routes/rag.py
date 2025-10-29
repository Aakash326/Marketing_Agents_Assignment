from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
import time
import logging
import sys
import os

logger = logging.getLogger(__name__)

# Ensure project root is on path from main.py; rag_system should be importable
create_qa_chain = None
import_error = None

try:
    from rag_system.src.retriever import create_qa_chain
    logger.info("Successfully imported RAG system")
except Exception as e:
    import_error = str(e)
    logger.error(f"Failed to import RAG system: {e}")
    logger.error(f"sys.path: {sys.path}")
    logger.error(f"cwd: {os.getcwd()}")

router = APIRouter()

class RAGQueryRequest(BaseModel):
    question: str
    k: Optional[int] = 3

class RAGQueryResponse(BaseModel):
    answer: str
    sources: List[str] = []
    retrieved_docs: List[Dict[str, Any]] = []
    processing_time: float

# Lazily initialized QA chain
_QA_CHAIN = None


def _get_chain():
    global _QA_CHAIN
    if _QA_CHAIN is not None:
        return _QA_CHAIN

    if create_qa_chain is None:
        logger.error("RAG import failure: rag_system not available")
        return None

    _QA_CHAIN = create_qa_chain()
    if _QA_CHAIN is None:
        logger.error("RAG QA chain could not be created (vector store or LLM missing)")
    return _QA_CHAIN


@router.get("/rag/status")
async def rag_status():
    """Check RAG system status."""
    return {
        "import_successful": create_qa_chain is not None,
        "import_error": import_error,
        "sys_path": sys.path[:3],
        "cwd": os.getcwd()
    }


@router.post("/rag/query", response_model=RAGQueryResponse)
async def rag_query(payload: RAGQueryRequest):
    """Answer general stock market questions using the existing vector store."""
    start = time.time()

    chain = _get_chain()
    if chain is None:
        error_msg = f"RAG is unavailable. Import error: {import_error}" if import_error else "RAG is unavailable. Ensure vectorstore exists and OpenAI API key is set."
        raise HTTPException(status_code=503, detail=error_msg)

    try:
        # LangChain RetrievalQA expects input key 'query'
        result = chain.invoke({"query": payload.question})

        answer = result.get("result") or result.get("answer") or ""
        src_docs = result.get("source_documents") or []

        # Build sources list and retrieved docs payload
        sources: List[str] = []
        retrieved_docs: List[Dict[str, Any]] = []

        for doc in src_docs:
            meta = getattr(doc, 'metadata', {}) or {}
            text = getattr(doc, 'page_content', '') or getattr(doc, 'text', '')
            source = meta.get('source') or meta.get('url') or meta.get('path') or "Unknown"
            if source not in sources:
                sources.append(source)
            retrieved_docs.append({
                "text": text[:500],
                "metadata": meta,
                "score": meta.get('score', None)
            })

        processing_time = round(time.time() - start, 3)
        return RAGQueryResponse(
            answer=answer.strip(),
            sources=sources,
            retrieved_docs=retrieved_docs,
            processing_time=processing_time
        )

    except Exception as e:
        logger.exception("RAG query failed")
        raise HTTPException(status_code=500, detail=f"RAG query failed: {str(e)}")
