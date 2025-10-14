"""
Simple RAG implementation using ChromaDB.
Stores documents and enables semantic search.
"""

import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict
import os


class SimpleKnowledgeBase:
    """Simple knowledge base using ChromaDB"""

    def __init__(self, persist_directory: str = "./knowledge_base"):
        """Initialize knowledge base"""
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)

        # Use sentence transformers for embeddings (free, no API key needed)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

        # Create/load ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="portfolio_knowledge",
            embedding_function=self.embedding_fn
        )

    def add_document(self, text: str, metadata: Dict, doc_id: str):
        """
        Add a document to the knowledge base.

        Args:
            text: Document text content
            metadata: Dictionary with document metadata (type, ticker, date, etc.)
            doc_id: Unique identifier for the document
        """
        try:
            # Split into chunks if text is too long
            max_chunk_size = 1000
            if len(text) > max_chunk_size:
                chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
            else:
                chunks = [text]

            # Add each chunk
            for i, chunk in enumerate(chunks[:10]):  # Limit to 10 chunks per doc
                chunk_id = f"{doc_id}_chunk_{i}"
                self.collection.add(
                    documents=[chunk],
                    metadatas=[metadata],
                    ids=[chunk_id]
                )

            return True
        except Exception as e:
            print(f"Error adding document: {e}")
            return False

    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Search the knowledge base.

        Args:
            query: Search query
            n_results: Number of results to return

        Returns:
            List of matching documents with text and metadata
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )

            # Format results
            documents = []
            if results['documents'] and len(results['documents']) > 0:
                for i, doc in enumerate(results['documents'][0]):
                    documents.append({
                        'text': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {}
                    })

            return documents
        except Exception as e:
            print(f"Error searching: {e}")
            return []

    def get_stats(self) -> Dict:
        """Get knowledge base statistics"""
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "collection_name": self.collection.name
            }
        except:
            return {"total_documents": 0}

    def clear(self):
        """Clear all documents from the knowledge base"""
        try:
            self.client.delete_collection(name="portfolio_knowledge")
            self.collection = self.client.get_or_create_collection(
                name="portfolio_knowledge",
                embedding_function=self.embedding_fn
            )
            return True
        except Exception as e:
            print(f"Error clearing knowledge base: {e}")
            return False
