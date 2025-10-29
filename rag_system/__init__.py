"""
RAG (Retrieval-Augmented Generation) System for Stock Market Knowledge

This package provides a complete RAG pipeline for educational stock market content,
enabling intelligent question-answering powered by vector search and LLMs.

Components:
- data_loader: Web scraping and content collection
- docs_loader: Document processing and chunking
- embedding: Text embedding models
- vector_store: ChromaDB vector database manager
- llm: LLM interface for generation
- retriever: Query and retrieval system
- pipeline: Main RAG orchestrator
- config: Configuration settings
"""

__version__ = "1.0.0"
__all__ = [
    "RAGPipeline",
    "DataLoader",
    "DocsLoader",
    "EmbeddingModel",
    "VectorStore",
    "LLMInterface",
    "Retriever",
]
