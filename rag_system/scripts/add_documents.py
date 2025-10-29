#!/usr/bin/env python3
"""
Script to add new documents to the RAG knowledge base.
Supports PDF and TXT files.

Usage:
    python add_documents.py --input path/to/document.pdf
    python add_documents.py --input path/to/folder/
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import argparse
from rag_system.src.pdf_loader import load_pdf
from rag_system.src.data_loader import load_text_file
from rag_system.src.document_processor import process_documents
from rag_system.src.vector_store import create_vector_store


def add_documents(input_path: str, rebuild: bool = False):
    """
    Add documents to the RAG knowledge base.
    
    Args:
        input_path: Path to PDF/TXT file or directory
        rebuild: If True, rebuild entire vector store. If False, add to existing.
    """
    path = Path(input_path)
    documents = []
    
    if not path.exists():
        print(f"❌ Error: Path does not exist: {input_path}")
        return
    
    # Load documents
    if path.is_file():
        print(f"📄 Loading file: {path.name}")
        if path.suffix.lower() == '.pdf':
            docs = load_pdf(str(path))
        elif path.suffix.lower() == '.txt':
            docs = load_text_file(str(path))
        else:
            print(f"❌ Unsupported file type: {path.suffix}")
            return
        documents.extend(docs)
    
    elif path.is_dir():
        print(f"📁 Loading documents from directory: {path}")
        for file in path.rglob('*'):
            if file.is_file():
                try:
                    if file.suffix.lower() == '.pdf':
                        print(f"  📄 Loading PDF: {file.name}")
                        docs = load_pdf(str(file))
                        documents.extend(docs)
                    elif file.suffix.lower() == '.txt':
                        print(f"  📄 Loading TXT: {file.name}")
                        docs = load_text_file(str(file))
                        documents.extend(docs)
                except Exception as e:
                    print(f"  ⚠️ Error loading {file.name}: {e}")
    
    if not documents:
        print("❌ No documents loaded!")
        return
    
    print(f"\n✅ Loaded {len(documents)} document chunks")
    
    # Process documents
    print("\n🔄 Processing documents...")
    processed_docs = process_documents(documents)
    
    # Create/update vector store
    print("\n🔄 Creating vector embeddings...")
    vector_store = create_vector_store(
        processed_docs,
        persist_directory=str(project_root / "vectorstore" / "db_faiss"),
        rebuild=rebuild
    )
    
    print(f"\n✅ Successfully added documents to knowledge base!")
    print(f"📊 Total documents in vector store: {len(processed_docs)}")
    print(f"💾 Vector store location: {project_root / 'vectorstore' / 'db_faiss'}")


def main():
    parser = argparse.ArgumentParser(
        description="Add documents to RAG knowledge base",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add a single PDF
  python add_documents.py --input documents/stock_basics.pdf
  
  # Add all files from a directory
  python add_documents.py --input documents/
  
  # Rebuild entire knowledge base
  python add_documents.py --input documents/ --rebuild
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Path to PDF/TXT file or directory containing documents'
    )
    
    parser.add_argument(
        '--rebuild', '-r',
        action='store_true',
        help='Rebuild entire vector store (default: add to existing)'
    )
    
    args = parser.parse_args()
    
    print("🚀 RAG Knowledge Base Document Adder")
    print("=" * 50)
    
    add_documents(args.input, args.rebuild)


if __name__ == "__main__":
    main()
