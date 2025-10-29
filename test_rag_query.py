"""
Test RAG System - Query the knowledge base
"""
from rag_system.src.retriever import create_qa_chain

def test_rag_queries():
    print("=" * 80)
    print("TESTING RAG SYSTEM")
    print("=" * 80)

    # Create QA chain
    print("\n1. Loading QA chain...")
    qa_chain = create_qa_chain()

    if not qa_chain:
        print("❌ Failed to create QA chain")
        return

    print("✅ QA chain loaded successfully!\n")

    # Test queries
    test_questions = [
        "What is a P/E ratio?",
        "What is a stock?",
        "How do stocks differ from bonds?",
        "What are the main types of stocks?",
    ]

    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*80}")
        print(f"Query {i}: {question}")
        print("=" * 80)

        try:
            result = qa_chain({"query": question})

            print(f"\n📝 Answer:")
            print(result['result'])

            if result.get('source_documents'):
                print(f"\n📚 Sources ({len(result['source_documents'])} documents):")
                for idx, doc in enumerate(result['source_documents'][:2], 1):
                    source = doc.metadata.get('source', 'Unknown')
                    print(f"  {idx}. Source: {source}")
                    print(f"     Preview: {doc.page_content[:100]}...")

        except Exception as e:
            print(f"❌ Error: {e}")

    print("\n" + "=" * 80)
    print("✅ RAG SYSTEM TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    test_rag_queries()
